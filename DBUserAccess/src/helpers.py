import strs
from logs import Log


from random import randint
import subprocess
import shlex


class Helpers (object):

	@classmethod
	def printList(cls, input_list):
		for item in input_list:
			print str(item)

	@classmethod
	def displayText(cls, input_text):
		try:
			print(str(input_text))
		except Exception, e:
			Log.writeLog('Error printing text. Msg : ' + str(e), strs.INFO)

	@classmethod
	def scramblePwd(cls, mode, plain_pwd, enc_pwd):

		
		if mode == strs.encrypt :
			Log.writeLog('encryption module is disabled.', strs.INFO)
			pass
			# random_int = randint(0000000000, 9999999999)
			# cmd_string = './bin/scramble.out "{0:s}"    "{1:s}"       "{2:s}"'.format(plain_pwd, "   ", random_int)
			# print cmd_string
			# scramble_cmd = subprocess.Popen(shlex.split(cmd_string), stdout=subprocess.PIPE)

			# return scramble_cmd.stdout
		elif mode == strs.decrypt :
			cmd_string = './bin/scramble.out "{0:s}" "{1:s}" "{2:s}"'.format("   ", enc_pwd.strip(), "   ")
			scramble_cmd = subprocess.Popen(shlex.split(cmd_string), stdout=subprocess.PIPE)			
			for line in scramble_cmd.stdout:
				plain_pwd = line[10:]
				scramble_cmd.communicate()				
				return plain_pwd.replace('\n', '').strip()
		else:
			"""
			noting to do
			"""
			return None

	@classmethod
	def getColumnList(cls, input_resultset):
		"""
		We return the list of columns in the input_resultset

		rtype: list, None
		"""
		col_list = []
		try:
			col_desc = input_resultset.description
			col_count = len(col_desc)
		except Exception, e:
			Log.writeLog('Exception in Helpers.getColumnList module. Msg : ' + str(e), strs.ERRO)
			return col_list

		
		

		for col in range(col_count):
			col_list.append(col_desc[col][0])

		return col_list


	@classmethod
	def writeToFile(cls, file_name, content):
		"""
		Writes content to the file, file_name

		rtype: 1 success , 0 fail
		"""

		try:
			file = open(file_name, 'a')
			file.write(str(content) + '\n')
			file.close()
			return 1

		except Exception, e:
			print('Exception in Helpers.displayText module. Msg: \n'+str(e))
			Log.writeLog('Exception in Helpers.writeToFile module. Msg: \n'+str(e), strs.ERRO)
			return 0
