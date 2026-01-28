# =============================================================================
# ASIGT Applicability Processor
# ACT/PCT/CCT applicability processing for S1000D
# Version: 2.0.0
# =============================================================================
"""
Applicability Processor

Processes S1000D applicability using:
    - ACT (Applicability Cross-reference Table)
    - PCT (Product Cross-reference Table)
    - CCT (Conditions Cross-reference Table)

Handles effectivity filtering, variant management, and applicability
annotation for Data Modules.

S1000D Applicability Model:
    ACT defines the applicability schema (what properties exist)
    PCT defines product instances (specific aircraft)
    CCT defines conditions (operational states)
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union

logger = logging.getLogger(__name__)


class ApplicabilityType(Enum):
    """Types of applicability."""
    PRODUCT = "product"           # Based on product configuration
    CONDITION = "condition"       # Based on operational condition
    COMBINED = "combined"         # Product + condition


class OperatorType(Enum):
    """Logical operators for applicability expressions."""
    AND = "and"
    OR = "or"
    NOT = "not"


@dataclass
class ApplicabilityProperty:
    """
    ACT property definition.
    
    Defines a single applicability property (e.g., model, engine type).
    """
    id: str                         # Property identifier
    name: str                       # Human-readable name
    description: str = ""           # Property description
    data_type: str = "string"       # string, integer, boolean
    enumerated_values: List[str] = field(default_factory=list)
    default_value: Optional[str] = None
    
    def validate_value(self, value: Any) -> bool:
        """Validate a value against this property definition."""
        if self.enumerated_values and value not in self.enumerated_values:
            return False
        
        if self.data_type == "integer":
            try:
                int(value)
            except (ValueError, TypeError):
                return False
        elif self.data_type == "boolean":
            if value not in (True, False, "true", "false", "1", "0"):
                return False
        
        return True


@dataclass
class ProductInstance:
    """
    PCT product instance definition.
    
    Represents a specific product configuration (e.g., aircraft serial number).
    """
    id: str                         # Instance identifier (e.g., serial number)
    name: str                       # Human-readable name
    properties: Dict[str, Any] = field(default_factory=dict)  # Property values
    
    def matches(self, criteria: Dict[str, Any]) -> bool:
        """Check if this instance matches the given criteria."""
        for prop, value in criteria.items():
            if prop not in self.properties:
                return False
            if self.properties[prop] != value:
                return False
        return True


@dataclass
class Condition:
    """
    CCT condition definition.
    
    Represents an operational condition (e.g., "engine running").
    """
    id: str                         # Condition identifier
    name: str                       # Human-readable name
    description: str = ""           # Condition description
    expression: Optional[str] = None  # Boolean expression


@dataclass
class ApplicabilityAnnotation:
    """
    Applicability annotation for a Data Module.
    
    Defines which products/conditions a DM applies to.
    """
    dm_code: str                    # Data Module code
    display_text: str = ""          # Human-readable applicability text
    applicable_products: Set[str] = field(default_factory=set)
    applicable_conditions: Set[str] = field(default_factory=set)
    expression: Optional[str] = None  # Full applicability expression
    
    def to_xml_element(self) -> str:
        """Generate S1000D applicability XML element."""
        lines = ['<applic>']
        
        if self.display_text:
            lines.append(f'  <displayText><simplePara>{self.display_text}</simplePara></displayText>')
        
        # Generate evaluate statement if we have products
        if self.applicable_products:
            products_list = " or ".join(
                f'prodattr[@applicPropertyIdent="serialno"]/@applicPropertyValue = "{p}"'
                for p in self.applicable_products
            )
            lines.append(f'  <evaluate>')
            lines.append(f'    <assert test="{products_list}"/>')
            lines.append(f'  </evaluate>')
        
        lines.append('</applic>')
        return "\n".join(lines)


@dataclass
class FilterResult:
    """Result of applicability filtering."""
    input_count: int
    output_count: int
    filtered_out: int
    applicable_items: List[str] = field(default_factory=list)
    excluded_items: List[str] = field(default_factory=list)
    filter_criteria: Dict[str, Any] = field(default_factory=dict)


class ACT:
    """
    Applicability Cross-reference Table.
    
    Defines the applicability property schema for the project.
    """
    
    def __init__(
        self,
        model_code: str,
        properties: Optional[List[ApplicabilityProperty]] = None,
    ):
        """
        Initialize ACT.
        
        Args:
            model_code: Aircraft model code
            properties: Initial property definitions
        """
        self.model_code = model_code
        self.properties: Dict[str, ApplicabilityProperty] = {}
        
        # Add default S1000D properties
        self._add_default_properties()
        
        # Add custom properties
        if properties:
            for prop in properties:
                self.add_property(prop)
    
    def _add_default_properties(self) -> None:
        """Add standard S1000D applicability properties."""
        default_props = [
            ApplicabilityProperty(
                id="model",
                name="Aircraft Model",
                description="Aircraft model designation",
            ),
            ApplicabilityProperty(
                id="serialno",
                name="Serial Number",
                description="Aircraft serial number",
            ),
            ApplicabilityProperty(
                id="effectivity",
                name="Effectivity Range",
                description="Serial number effectivity range",
            ),
            ApplicabilityProperty(
                id="engine",
                name="Engine Type",
                description="Installed engine type",
            ),
            ApplicabilityProperty(
                id="config",
                name="Configuration",
                description="Aircraft configuration variant",
            ),
            ApplicabilityProperty(
                id="mod",
                name="Modification Status",
                description="Applied modification status",
            ),
            ApplicabilityProperty(
                id="sb",
                name="Service Bulletin",
                description="Applied service bulletin status",
            ),
        ]
        
        for prop in default_props:
            self.properties[prop.id] = prop
    
    def add_property(self, prop: ApplicabilityProperty) -> None:
        """Add a property to the ACT."""
        self.properties[prop.id] = prop
        logger.debug(f"Added ACT property: {prop.id}")
    
    def get_property(self, prop_id: str) -> Optional[ApplicabilityProperty]:
        """Get property by ID."""
        return self.properties.get(prop_id)
    
    def validate_property_value(self, prop_id: str, value: Any) -> bool:
        """Validate a value for a property."""
        prop = self.properties.get(prop_id)
        if not prop:
            return False
        return prop.validate_value(value)
    
    def to_xml(self) -> str:
        """Generate S1000D ACT XML."""
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<act xmlns="http://www.s1000d.org/S1000D_5-0">',
            '  <identAndStatusSection>',
            '    <!-- ACT identification -->',
            '  </identAndStatusSection>',
            '  <content>',
            '    <applicCrossRefTable>',
        ]
        
        for prop in self.properties.values():
            lines.append(f'      <applicProperty applicPropertyIdent="{prop.id}"')
            lines.append(f'                      applicPropertyType="{prop.data_type}">')
            lines.append(f'        <name>{prop.name}</name>')
            if prop.description:
                lines.append(f'        <description>{prop.description}</description>')
            if prop.enumerated_values:
                lines.append('        <enumeration>')
                for val in prop.enumerated_values:
                    lines.append(f'          <enumValue>{val}</enumValue>')
                lines.append('        </enumeration>')
            lines.append('      </applicProperty>')
        
        lines.extend([
            '    </applicCrossRefTable>',
            '  </content>',
            '</act>',
        ])
        
        return "\n".join(lines)


class PCT:
    """
    Product Cross-reference Table.
    
    Defines specific product instances (aircraft configurations).
    """
    
    def __init__(
        self,
        model_code: str,
        act: ACT,
        instances: Optional[List[ProductInstance]] = None,
    ):
        """
        Initialize PCT.
        
        Args:
            model_code: Aircraft model code
            act: Associated ACT
            instances: Initial product instances
        """
        self.model_code = model_code
        self.act = act
        self.instances: Dict[str, ProductInstance] = {}
        
        if instances:
            for instance in instances:
                self.add_instance(instance)
    
    def add_instance(self, instance: ProductInstance) -> bool:
        """
        Add a product instance to the PCT.
        
        Args:
            instance: Product instance to add
            
        Returns:
            True if added successfully
        """
        # Validate properties against ACT
        for prop_id, value in instance.properties.items():
            if not self.act.validate_property_value(prop_id, value):
                logger.warning(
                    f"Invalid property value for {prop_id}: {value}"
                )
                return False
        
        self.instances[instance.id] = instance
        logger.debug(f"Added PCT instance: {instance.id}")
        return True
    
    def get_instance(self, instance_id: str) -> Optional[ProductInstance]:
        """Get product instance by ID."""
        return self.instances.get(instance_id)
    
    def find_instances(self, criteria: Dict[str, Any]) -> List[ProductInstance]:
        """
        Find instances matching criteria.
        
        Args:
            criteria: Property criteria to match
            
        Returns:
            List of matching instances
        """
        return [
            inst for inst in self.instances.values()
            if inst.matches(criteria)
        ]
    
    def to_xml(self) -> str:
        """Generate S1000D PCT XML."""
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<pct xmlns="http://www.s1000d.org/S1000D_5-0">',
            '  <identAndStatusSection>',
            '    <!-- PCT identification -->',
            '  </identAndStatusSection>',
            '  <content>',
            '    <productCrossRefTable>',
        ]
        
        for instance in self.instances.values():
            lines.append(f'      <product productIdent="{instance.id}">')
            lines.append(f'        <name>{instance.name}</name>')
            for prop_id, value in instance.properties.items():
                lines.append(f'        <assign applicPropertyIdent="{prop_id}"')
                lines.append(f'                applicPropertyValue="{value}"/>')
            lines.append('      </product>')
        
        lines.extend([
            '    </productCrossRefTable>',
            '  </content>',
            '</pct>',
        ])
        
        return "\n".join(lines)


class CCT:
    """
    Conditions Cross-reference Table.
    
    Defines operational conditions for applicability.
    """
    
    def __init__(
        self,
        model_code: str,
        conditions: Optional[List[Condition]] = None,
    ):
        """
        Initialize CCT.
        
        Args:
            model_code: Aircraft model code
            conditions: Initial conditions
        """
        self.model_code = model_code
        self.conditions: Dict[str, Condition] = {}
        
        # Add default conditions
        self._add_default_conditions()
        
        if conditions:
            for cond in conditions:
                self.add_condition(cond)
    
    def _add_default_conditions(self) -> None:
        """Add common operational conditions."""
        default_conditions = [
            Condition(
                id="COND-001",
                name="Aircraft on Jacks",
                description="Aircraft is supported on jacks",
            ),
            Condition(
                id="COND-002",
                name="Engine Running",
                description="Engine is running",
            ),
            Condition(
                id="COND-003",
                name="Power On",
                description="Aircraft electrical power is on",
            ),
            Condition(
                id="COND-004",
                name="Hydraulic Pressure Available",
                description="Hydraulic system is pressurized",
            ),
            Condition(
                id="COND-005",
                name="Aircraft Depressurized",
                description="Cabin is depressurized",
            ),
        ]
        
        for cond in default_conditions:
            self.conditions[cond.id] = cond
    
    def add_condition(self, condition: Condition) -> None:
        """Add a condition to the CCT."""
        self.conditions[condition.id] = condition
        logger.debug(f"Added CCT condition: {condition.id}")
    
    def get_condition(self, cond_id: str) -> Optional[Condition]:
        """Get condition by ID."""
        return self.conditions.get(cond_id)
    
    def to_xml(self) -> str:
        """Generate S1000D CCT XML."""
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<cct xmlns="http://www.s1000d.org/S1000D_5-0">',
            '  <identAndStatusSection>',
            '    <!-- CCT identification -->',
            '  </identAndStatusSection>',
            '  <content>',
            '    <condCrossRefTable>',
        ]
        
        for cond in self.conditions.values():
            lines.append(f'      <cond condIdent="{cond.id}">')
            lines.append(f'        <name>{cond.name}</name>')
            if cond.description:
                lines.append(f'        <description>{cond.description}</description>')
            lines.append('      </cond>')
        
        lines.extend([
            '    </condCrossRefTable>',
            '  </content>',
            '</cct>',
        ])
        
        return "\n".join(lines)


class ApplicabilityProcessor:
    """
    S1000D Applicability Processor.
    
    Processes ACT/PCT/CCT for applicability filtering and annotation
    of Data Modules. Operates under ASIT contract authority.
    
    Attributes:
        contract: ASIT transformation contract
        config: Processor configuration
        act: Applicability Cross-reference Table
        pct: Product Cross-reference Table
        cct: Conditions Cross-reference Table
        
    Example:
        >>> processor = ApplicabilityProcessor(contract=contract, config=config)
        >>> processor.add_product("SN001", {"model": "HJ1", "engine": "CFM1"})
        >>> filtered = processor.filter_by_product(dm_list, product_id="SN001")
    """
    
    def __init__(
        self,
        contract: Dict[str, Any],
        config: Dict[str, Any],
    ):
        """
        Initialize Applicability Processor.
        
        Args:
            contract: ASIT transformation contract (required)
            config: Processor configuration
            
        Raises:
            ValueError: If contract is missing
        """
        if not contract:
            raise ValueError("ASIT contract is required for applicability processing")
        
        self.contract = contract
        self.config = config
        
        # Extract configuration
        self.contract_id = contract.get("id", "UNKNOWN")
        self.model_code = config.get("model_ident_code", "XXX")
        
        # Initialize ACT/PCT/CCT
        self.act = ACT(self.model_code)
        self.pct = PCT(self.model_code, self.act)
        self.cct = CCT(self.model_code)
        
        logger.info(
            f"ApplicabilityProcessor initialized: contract={self.contract_id}"
        )
    
    def add_property(
        self,
        prop_id: str,
        name: str,
        description: str = "",
        data_type: str = "string",
        enumerated_values: Optional[List[str]] = None,
    ) -> None:
        """
        Add a custom applicability property to the ACT.
        
        Args:
            prop_id: Property identifier
            name: Human-readable name
            description: Property description
            data_type: Data type (string, integer, boolean)
            enumerated_values: Optional list of allowed values
        """
        prop = ApplicabilityProperty(
            id=prop_id,
            name=name,
            description=description,
            data_type=data_type,
            enumerated_values=enumerated_values or [],
        )
        self.act.add_property(prop)
    
    def add_product(
        self,
        product_id: str,
        name: str,
        properties: Dict[str, Any],
    ) -> bool:
        """
        Add a product instance to the PCT.
        
        Args:
            product_id: Product identifier (e.g., serial number)
            name: Human-readable name
            properties: Property values
            
        Returns:
            True if added successfully
        """
        instance = ProductInstance(
            id=product_id,
            name=name,
            properties=properties,
        )
        return self.pct.add_instance(instance)
    
    def add_condition(
        self,
        cond_id: str,
        name: str,
        description: str = "",
    ) -> None:
        """
        Add a condition to the CCT.
        
        Args:
            cond_id: Condition identifier
            name: Human-readable name
            description: Condition description
        """
        cond = Condition(
            id=cond_id,
            name=name,
            description=description,
        )
        self.cct.add_condition(cond)
    
    def filter_by_product(
        self,
        items: List[Dict[str, Any]],
        product_id: str,
    ) -> FilterResult:
        """
        Filter items by product applicability.
        
        Args:
            items: List of items (DMs, etc.) with applicability
            product_id: Target product identifier
            
        Returns:
            FilterResult with applicable items
        """
        product = self.pct.get_instance(product_id)
        if not product:
            logger.warning(f"Product not found: {product_id}")
            return FilterResult(
                input_count=len(items),
                output_count=0,
                filtered_out=len(items),
                filter_criteria={"product_id": product_id},
            )
        
        applicable = []
        excluded = []
        
        for item in items:
            item_id = item.get("dm_code", item.get("id", "unknown"))
            item_applicability = item.get("applicability", {})
            
            # Check if item applies to this product
            if self._item_applies_to_product(item_applicability, product):
                applicable.append(item_id)
            else:
                excluded.append(item_id)
        
        return FilterResult(
            input_count=len(items),
            output_count=len(applicable),
            filtered_out=len(excluded),
            applicable_items=applicable,
            excluded_items=excluded,
            filter_criteria={"product_id": product_id},
        )
    
    def filter_by_effectivity(
        self,
        items: List[Dict[str, Any]],
        serial_from: int,
        serial_to: Optional[int] = None,
    ) -> FilterResult:
        """
        Filter items by serial number effectivity range.
        
        Args:
            items: List of items with effectivity
            serial_from: Starting serial number
            serial_to: Ending serial number (optional)
            
        Returns:
            FilterResult with applicable items
        """
        applicable = []
        excluded = []
        
        for item in items:
            item_id = item.get("dm_code", item.get("id", "unknown"))
            item_effectivity = item.get("effectivity", {})
            
            if self._check_effectivity(item_effectivity, serial_from, serial_to):
                applicable.append(item_id)
            else:
                excluded.append(item_id)
        
        return FilterResult(
            input_count=len(items),
            output_count=len(applicable),
            filtered_out=len(excluded),
            applicable_items=applicable,
            excluded_items=excluded,
            filter_criteria={
                "serial_from": serial_from,
                "serial_to": serial_to,
            },
        )
    
    def annotate_dm(
        self,
        dm_code: str,
        products: Optional[List[str]] = None,
        conditions: Optional[List[str]] = None,
        display_text: Optional[str] = None,
    ) -> ApplicabilityAnnotation:
        """
        Create applicability annotation for a Data Module.
        
        Args:
            dm_code: Data Module code
            products: List of applicable product IDs
            conditions: List of applicable condition IDs
            display_text: Human-readable applicability text
            
        Returns:
            ApplicabilityAnnotation
        """
        # Build display text if not provided
        if not display_text and products:
            product_names = []
            for p_id in products:
                product = self.pct.get_instance(p_id)
                if product:
                    product_names.append(product.name)
                else:
                    product_names.append(p_id)
            display_text = "Applicable to: " + ", ".join(product_names)
        
        return ApplicabilityAnnotation(
            dm_code=dm_code,
            display_text=display_text or "All",
            applicable_products=set(products or []),
            applicable_conditions=set(conditions or []),
        )
    
    def parse_effectivity_string(
        self,
        effectivity: str,
    ) -> List[Tuple[int, Optional[int]]]:
        """
        Parse effectivity string into ranges.
        
        Handles formats like:
            - "001-100"
            - "001-050, 075-100"
            - "001 AND ON"
            
        Args:
            effectivity: Effectivity string
            
        Returns:
            List of (from, to) tuples
        """
        ranges = []
        
        # Handle "AND ON" syntax
        if "AND ON" in effectivity.upper():
            match = re.search(r"(\d+)\s*AND\s*ON", effectivity.upper())
            if match:
                ranges.append((int(match.group(1)), None))
                return ranges
        
        # Handle comma-separated ranges
        parts = effectivity.split(",")
        for part in parts:
            part = part.strip()
            
            # Handle range (e.g., "001-100")
            if "-" in part:
                from_to = part.split("-")
                try:
                    ranges.append((int(from_to[0]), int(from_to[1])))
                except (ValueError, IndexError):
                    continue
            
            # Handle single value
            else:
                try:
                    val = int(part)
                    ranges.append((val, val))
                except ValueError:
                    continue
        
        return ranges
    
    def generate_act_xml(self) -> str:
        """Generate S1000D ACT XML."""
        return self.act.to_xml()
    
    def generate_pct_xml(self) -> str:
        """Generate S1000D PCT XML."""
        return self.pct.to_xml()
    
    def generate_cct_xml(self) -> str:
        """Generate S1000D CCT XML."""
        return self.cct.to_xml()
    
    def _item_applies_to_product(
        self,
        item_applicability: Dict[str, Any],
        product: ProductInstance,
    ) -> bool:
        """Check if item applies to a specific product."""
        # If no applicability specified, applies to all
        if not item_applicability:
            return True
        
        # Check product list
        applicable_products = item_applicability.get("products", [])
        if applicable_products and product.id not in applicable_products:
            return False
        
        # Check property criteria
        criteria = item_applicability.get("criteria", {})
        for prop, value in criteria.items():
            if prop in product.properties:
                if product.properties[prop] != value:
                    return False
        
        return True
    
    def _check_effectivity(
        self,
        item_effectivity: Dict[str, Any],
        serial_from: int,
        serial_to: Optional[int],
    ) -> bool:
        """Check if serial range is within item effectivity."""
        # If no effectivity specified, applies to all
        if not item_effectivity:
            return True
        
        item_from = item_effectivity.get("from")
        item_to = item_effectivity.get("to")
        
        # Parse effectivity string if present
        eff_string = item_effectivity.get("string")
        if eff_string:
            ranges = self.parse_effectivity_string(eff_string)
            for range_from, range_to in ranges:
                if range_to is None:
                    # "AND ON" - applies from range_from onwards
                    if serial_from >= range_from:
                        return True
                else:
                    # Check overlap
                    if serial_to is None:
                        serial_to = serial_from
                    if serial_from <= range_to and serial_to >= range_from:
                        return True
            return False
        
        # Simple from/to check
        if item_from is not None and serial_from < item_from:
            return False
        if item_to is not None:
            check_to = serial_to if serial_to is not None else serial_from
            if check_to > item_to:
                return False
        
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get processor statistics."""
        return {
            "contract_id": self.contract_id,
            "model_code": self.model_code,
            "act_properties": len(self.act.properties),
            "pct_products": len(self.pct.instances),
            "cct_conditions": len(self.cct.conditions),
        }
