"""Mapping for command invoke name to logic"""
from .commands import create_incident,get_incident,modify_incident,get_incidents,modify_state,states,close_incident,\
                      resolve_incident,close_code,delete_incident,show_priorities,change_priority,show_impact,change_impact\



commands_by_invoke_name = {
"createincident" : create_incident,
"getincident" : get_incident,
"modifyincident" : modify_incident,
"getincidents"  : get_incidents,
"modifystate" : modify_state,
"states" : states,
"closeincident": close_incident,
"resolveincident": resolve_incident,
"closecode": close_code,
"deleteincident": delete_incident,
"showpriorities": show_priorities,
"changepriority": change_priority,
"showimpact": show_impact,
"changeimpact": change_impact,

}
