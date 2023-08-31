    def swapBootstrapping(self,data:pd.DataFrame):
        swapTrans = data.transpose()
        rows, columns = swapTrans.shape
        nrows = rows
        ncolumns = columns
        P_t_Tn = pd.DataFrame(np.zeros((nrows, ncolumns))) 
        ZeroData = pd.DataFrame(np.zeros((nrows, ncolumns)))
        ZeroData.index = swapTrans.index
        ZeroData.iloc[0] = swapTrans.iloc[0]
        
        # Prima riga
        for row in range(0, 1):
            for column in range(ncolumns):
                i_t_Ti = swapTrans.iloc[row, column] 
                P_t_Ti = (1 + i_t_Ti) ** - (row+1)
                P_t_Tn.iloc[row, column] = P_t_Ti
        # Righe successive
        for row in range(1, nrows):
            for column in range(ncolumns):
                i_t_Ti = swapTrans.iloc[row, column]
                up_sum = P_t_Tn.iloc[0:row, column].sum()
                P_t_Ti = (1 - (i_t_Ti * up_sum)) / (1 + i_t_Ti)
                P_t_Tn.iloc[row, column] = P_t_Ti
                if P_t_Tn.iloc[row, column] < 0:
                    print(
                        f'Attenzione: il {row-2} nodo della SWAP risulta negativo in quanto, nel bootstrapping, a numeratore \
                              [1 - (tasso swap * sommatoria)] troviamo il valore negativo (1 - {i_t_Ti} * {up_sum}). Pertanto, nella \
                                formula di bootstrapping esce un esponenziale a base negativa che da un risultato non reale (NaN in python, !VALORE in excel)'
                        )

        for row in range(1, nrows):
            for column in range(ncolumns):
                P_t_Ti = P_t_Tn.iloc[row, column]
                zero_val = ((1 / P_t_Ti) ** (1/(row+1))) - 1
                ZeroData.iloc[row, column] = zero_val
        
        #Traspongo la tabella dei tassi Zero ed elimino le colonne che non mi servono
        ZeroTrans = ZeroData.transpose()

        return ZeroTrans
