from app.schemas import Filter, MatchMode
from typing import Dict, Any
# from app.inventory.models import Product
# Product.cyclic_counts.property.instrument_class
def build_filter_clause(field, match_mode: MatchMode, value: Any ):
    #Might need to include model
    if match_mode == MatchMode.EQUALS:
        return (field == value)
    if match_mode == MatchMode.CONTAINS:    
        return (field.like(f"%{value}%"))
    if match_mode == MatchMode.IN:    
        return (field.in_(value))
    return None #Unknown filter usage
    

def filters_to_sqlalchemy(model ,filters: Dict[str, Filter]):
    sqlalch_filters = []
    original_attr = ""
    for attribute, filter in filters.items():
        if "." in attribute:
            continue
        else:
            original_attr = getattr(model, attribute) #will raise exception if not found

        if filter.value in (None, "", []) \
        and filter.match_mode not in (MatchMode.IS_EMPTY, MatchMode.IS_NOT_EMPTY, 
                                      MatchMode.EQUALS, MatchMode.NOT_EQUALS):
            continue
        
        result_filter = build_filter_clause(original_attr, filter.match_mode, filter.value)
        if result_filter is not None:
            sqlalch_filters.append(result_filter)
    return sqlalch_filters