######-------------bootstrap_out  -----------------------
def bootstrap_out(c_data,c_idx,f_name, rep):
    total_value = []
    total_value2 = []
    total_value3 = []

    # copy_data = c.deepcopy(x[max_idx])
    sample = c_data[0]

    for i in range(0, c_data.shape[0]):
        sample = np.append(sample, c_data[i])
		
        var_sample = sample.var()
        #     var_sample = s.mean(sample)
        boot = bootstrap(sample, rep)
		# len(cintervals)= 3
        cintervals = [boot(j) for j in (.90, .95, .99)]

        #         cintervals = [boot(i) for i in range(len(ci_range)-1) ]
        k = 0
        while k <= len(cintervals) - 1:
            # check whther a var is in the CI
            if (var_sample >= cintervals[k][0]) & (var_sample <= cintervals[k][1]):
                out = 1  ### print('Y')
            else:
                out = 0

            if k == 0:
                out_value = [i, var_sample, cintervals[k][0], cintervals[k][1], out]
                total_value.append(out_value)
            elif k == 1:
                out_value2 = [cintervals[k][0], cintervals[k][1], out]
                total_value2.append(out_value2)
            else:
                out_value3 = [cintervals[k][0], cintervals[k][1], out]
                total_value3.append(out_value3)

            k = k + 1
    #     out_value = [i,cintervals[0][0],cintervals[0][1],cintervals[1][0],cintervals[1][1],cintervals[2][0],cintervals[2][1]]

    #     out_value = [i,var_sample,ci_sample[0],ci_sample[1],out]
    total_value = pd.DataFrame(total_value)
    total_value2 = pd.DataFrame(total_value2)
    total_value3 = pd.DataFrame(total_value3)
    cg_idx = pd.DataFrame(c_idx[0:]) # index for change point

    all_CIs = pd.concat([cg_idx, total_value, total_value2, total_value3], axis=1)
    all_CIs.columns  = ['id', 'idx', 'var','.9Low', '.9up', 'out_9', '.95L', '.95U', 'out_95', '.99L', '.99U', 'out_99']
    out_name= f_name + '_' + str(rep) + '_bootstrapC'
    out_file_name = "%s.csv" % out_name
    # all_CIs=pd.DataFrame(all_CIs,columns=['idx','.9Low','.9up','out_9','.95L','.95U','out_95','.99L','.99U','out_99',])
    all_CIs.to_csv(out_file_name, index=False)
    # all_CIs.to_csv('bootstrapVar5000_CI_ratio.csv', index=False)

    return all_CIs