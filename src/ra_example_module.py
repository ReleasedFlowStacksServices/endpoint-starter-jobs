import sys, uuid, json
from datetime                       import datetime, date, timedelta

sys.path.append("/flowstacks/public-cloud-src")
from logger.logger import Logger
from modules.base_api.fs_web_tier_base_work_item     import FSWebTierBaseWorkItem
from connectors.redis.redis_pickle_application       import RedisPickleApplication

# FlowStacks Example Job:
# Out of convention FlowStacks REST API Jobs begin with "RA_"
class RA_ExampleModule(FSWebTierBaseWorkItem):

    def __init__(self, json_data):
        # The RA_ExampleModule becomes the prefix for the Job when it is logged by the system
        FSWebTierBaseWorkItem.__init__(self, "RA_ExampleModule", json_data)

        """ Constructor Serialization taking HTTP Post-ed JSON into Python members """
        # Define Inputs and Outputs for the Job to serialize over HTTP
        try:

            # INPUTS:
            self.m_input_key                        = json_data["This is an Input Key"]

            # OUTPUTS:
            self.m_results["Status"]                = "FAILED"
            self.m_results["Error"]                 = ""
            self.m_results["This is an Output Key"] = "NO OUTPUT"

            # MEMBERS:
        
        # Return the exact Error with the failure:
        except Exception,e:

            import os, traceback
            exc_type, exc_obj, exc_tb = sys.exc_info()
            reason = json.dumps({ "Module" : str(self.__class__.__name__), "Error Type" : str(exc_type.__name__), "Line Number" : exc_tb.tb_lineno, "Error Message" : str(exc_obj.message), "File Name" : str(os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]) })
            raise Exception(reason)


    # end of  __init__


###############################################################################
#
# Job Module Handle Each State Methods
#
###############################################################################


    def handle_startup(self):

        self.lg("Start Handle Module Startup", 5)

        self.m_state                = "Results"
        self.m_results["Status"]    = "FAILED"

        db_app_id   = 0
        for db_app in self.m_db_apps:

            self.lg("Job has Access to Database Application(" + str(db_app_id) + ") with Name(" + str(db_app) + ")", 5)
            db_app_id   += 1

        # end of for all Database Applications

        self.lg("Done Module Startup State(" + self.m_state + ")", 5)

        return None
    # end of handle_startup

    
    def handle_processing_results(self):

        self.lg("Processing Results", 5)

        # For this Example just show the Input can be set to the Output for testing
        self.m_results["Status"]                = "SUCCESS"
        self.m_results["This is an Output Key"] = str(self.m_input_key)

        self.lg("Done Processing Results", 5)

        return None
    # end of handle_processing_results


###############################################################################
#
# Helpers
#
###############################################################################


###############################################################################
#
# Job Module State Machine
#
###############################################################################


    # Add and Extend New States as Needed:
    def perform_task(self):

        if  self.m_state == "Startup":
            self.lg("Startup", 5)
            self.handle_startup()

        elif self.m_state == "Results":
            # found in the base
            self.lg("Result Cleanup", 5)
            self.handle_processing_results()
            self.base_handle_results_and_cleanup(self.m_result_details, self.m_completion_details)

        else:
            if self.m_log:
                self.lg("UNKNOWN STATE FOUND IN OBJECT(" + self.m_name + ") State(" + self.m_state + ")", 0)
            self.m_state = "Results"

        # end of State Loop
        return self.m_is_done
    # end of perform_task

# end of RA_ExampleModule


