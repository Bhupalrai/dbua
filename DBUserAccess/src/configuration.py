"""
Initializing class and configuration reader/verifier are implemented here
"""

import ConfigParser
from files import ReadFile

import strs
from logs import Log
from helpers import Helpers




class VerifyConfiguration(object):
    """
	All initial varification tasks are implemented here
	"""

    def __init__(self):
        # Verify metaserver configuratin file
        if not ReadFile().exists(strs.meta_svr_conf_file):
            Log.writeLog('configuration file doesnot exits', strs.ERRO)
            raise SystemExit('configuration file doesnot exits')

    def metaSvrConfFileVerify(self, config_file=strs.meta_svr_conf_file):
        """
		verify the content of the configuratin file
		"""
        pass


class ConfigReader(object):

    @classmethod
    def getLogLevel(cls):
        """
		Read the log level from config file

		rtype: numeric string
		"""

        config = ConfigParser.ConfigParser()

        try:
            config.read(strs.dbu_conf_file)
        except Exception, e:
            Log.writeLog('Error reading dbu_conf_file.cfg file. Msg : ' + str(e), strs.ERRO)
            raise SystemExit('Error reading dbu_conf_file.cfg file. Msg : ' + str(e))


        try:
            # print config.sections()
            return config.get(strs.dbu_conf_file_section_dbu_log, 'log_level')
        except Exception, e:
            Log.writeLog('Exception occured while reading log level. Msg : ' + str(e), strs.ERRO)
            return 0

    @classmethod
    def getMetaSvrAccessPara(cls):
        """
		rtype: dictionary
		"""
        config = ConfigParser.ConfigParser()

        try:
            config.read(strs.meta_svr_conf_file)
        except Exception, e:
            Helpers.displayText('Error reading meta_svr_conf_file.cfg file. Msg : ' + str(e))
            Log.writeLog('Error reading meta_svr_conf_file.cfg file. Msg : ' + str(e), strs.ERRO)
            raise SystemExit('Error reading meta_svr_conf_file.cfg file. Msg : ' + str(e))

        try:
            access_para_dict = {}
            for item in config.options(strs.meta_svr_conf_file_section_meta_svr_conf):
                access_para_dict[item] = config.get(strs.meta_svr_conf_file_section_meta_svr_conf, item)
            return access_para_dict
        except Exception, e:

            Helpers.displayText('Exception occured in configuration.getMetaSvrAccessPara module. Msg : ' + str(e))
            Log.writeLog('Exception occured in configuration.getMetaSvrAccessPara module. Msg : ' + str(e), strs.ERRO)
            raise SystemExit('Exception occured in configuration.getMetaSvrAccessPara module. Msg : ' + str(e))
            
            return 0
