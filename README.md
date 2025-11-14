可執行的python:

../ETM/run.py [exp_name] 
  根據experiments/[exp_name]/config.json設定跑實驗，並將結果儲存在experiments/[exp_name]/result/

../ETM/show_result.py [exp_name1, exp_name2, ...]  
  展示實驗結果

../ETM/trace/cut_trace.py [trace_name, cut_size]  
  裁剪trace長度

../ETM/trace/get_trace_info.py [trace_name] 
  計算trac特性(working set size, 請求數, 相異obj數)

../ETM/policies/ETM_AEP/ETM_labeling.py [exp_name] 
  將trace加上熱門度
  
../ETM/policies/ETM_AEP/label_check.py [exp_name] 
  展示預測熱門度與實際值差距

跑ETM實驗前需要先做ETM_labeling.py才可跑 run.py ETM_exp
