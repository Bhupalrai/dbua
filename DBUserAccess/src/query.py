import strs
from logs import Log
from configuration import ConfigReader


class Query :
    """
    Handle query related tasks
    :rtype : resultset
    """

    def executeQuery(self, query_string, conn):

        # Get query 
        self.cursor = conn.cursor()
        try:
            self.cursor.execute(query_string)    
        except Exception, e:
            Log.writeLog('Exception occured in query.executeQuery module. Msg : ' + str(e) + \
                '\n Query : ' + query_string, strs.ERRO)

            return 0

        return self.cursor 



    def convertResultToList(self, input_resultset, columns):
        """
        Convert resultset to list. 
        For two dimensional resultset, convert to list of list

        :rtype : list
        """
        
        self.cursor = input_resultset
        converted_to_list = []



        # convert everything to list
        tmp_init_query_result_list = self.cursor.fetchall()

        #
        # if query returns empty then return list with null values
        #
    

        for row_tuple in tmp_init_query_result_list: 
            tmp_row = []
            if len(columns) > 1 :            
                for column in columns :
                    tmp_row.append(row_tuple[columns.index(column)])
                converted_to_list.append(tmp_row)
            elif len(columns) == 1:
                converted_to_list.append(row_tuple[0])
            else:
                pass
        
        return converted_to_list  


    def getColumnsList(self, input_resultset):
        """
        return the column names in the resultset as a list
        :rtype : list
        """
        
        self.columns = []

        cursor = input_resultset
        # Get  columns and append it to list
        try:
            desc = cursor.description
            column_count = len(desc)
        except Exception, e:
            Log.writeLog('Exception in Query.getColumnsList module. Msg: ' + str(e), strs.ERRO)
            return self.columns

        

        # extract column names
        for col in range(column_count): 
            self.columns.append(desc[col][0])

        return self.columns



class MssqlQuery(Query):
    """
    The query execution of mssql
    """
    def executeQuery(self, query_string, conn):

        # Get query 
        self.cursor = conn.cursor()
        """
        Create procedure to extract information about sql
        """
        try:
            procedurecreate=strs.create_mssql_proc_inventry
            self.cursor.execute(strs.drop_inventry_if_exists)
            self.cursor.execute(procedurecreate)
        except Exception, e:
            Log.writeLog('Exception in MssqlQuery.executeQuery module. Msg : ' + str(e), strs.ERRO)
            return 0


        """
        execute procedure
        """
        try:
            callprocedure=strs.execute_inventry
            self.cursor.execute(callprocedure)            
        except Exception, e:
            Log.writeLog('Exception i MssqlQuery.executeQuery module. Msg : ' + str(e), strs.ERRO)
            return 0


        """
        drop the create procedure
        """
        try:
            dropprocedure=strs.drop_inventry
            self.cursor.execute(dropprocedure)
        except Exception, e:
            Log.writeLog('Exception in MssqlQuery.dropProcedure module. Msg : ' + str(e), strs.ERRO)
            return 0        



        """
        To call the result from procedure
        """
        try:            
            self.cursor.execute(query_string)

        except Exception, e:
            Log.writeLog('Exception occured in query.executeQuery module. Msg : ' + str(e) + \
               '\n Query : ' + query_string, strs.ERRO)
            return 0        
        return self.cursor  


    def dropProcedure(self,conn):        
        """
        To drop the procedure executed above
        """
        self.cursor=conn.cursor()
        
        try:
            dropprocedure=strs.drop_inventry
            self.cursor.execute(dropprocedure)
        except Exception, e:
            Log.writeLog('Exception in MssqlQuery.dropProcedure module. Msg : ' + str(e), strs.ERRO)
            return 0
