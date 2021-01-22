import pandas as pd
import numpy as np
arr = np.random.rand(4,2)
arr = np.asarray(arr,dtype="str")
df = pd.DataFrame(arr, index=list(range(arr.shape[0])),columns=["o","k"])

subjects = df.o.to_numpy()
res = '\n'.join(list(subjects))
print(res)


subjects = df.subject.to_numpy()
senders = df.sender.to_numpy()
receivers = df.receiver.to_numpy()

subjects = 'subjects: \n'+'\n'.join(list(subjects))
senders = 'senders: \n'+'\n'.join(list(senders))
receivers = 'receivers: \n'+'\n'.join(list(receivers))

