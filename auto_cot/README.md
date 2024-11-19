# Auto-CoT: Automatic Chain of Thought Prompting in Large Language Models (ICLR 2023)

<h2> 论文地址:https://arxiv.org/pdf/2210.03493.pdf </h2>

<h3>核心动机：能不能找出一个自动化方法，代替人工实现manual cot的效果？<br>

首先给一个问题的集合:<br>

1.随机方法，随便从集合里选k个问题,这是random-q-cot<br>

2.给一个测试问题，从集合里选和它类似的问题，这是retrieval-q-cot<br>

但是实验验证retrieval的效果最差，可能的原因：集合由zero-shot cot生成，有可能对于某一类问题的问答是错误的，retrieval从demo里学到错误的知识，错误的思维传递导致性能变差<br>

如何不让模型受到zero-shot错误理解的影响，可以看出错误的形式都比较像，最直接的方法是基于语义对问题，使用k-means聚成k个类，看zero-shot对每个类的错误率。发现总会有一个cluster的错误率特别高（有聚集现象）。<br>

每个类别中采样一个最具代表性的问题，输入到zero-shot得到推理链条。也就是说使用diverse的方法，放弃了retrieval那种similar方法，也放弃了random方法。<br>

首先对n个句子使用sentence BERT编码，得到对应句子集表示，之后把句子输入k-means聚成k个clusters，选择clusters里中心最近的问题（最具代表性），每个问题后拼上zero-shot提示词 （stepbystep），从而生成k个rationales。最后把questions和rationales对应拼起来得到k个demostrations，把这些作为上下文输入给语言模型进行推理。最后能超过manual cot<h3>
## multiarith聚类图
![multiarith.png](demos%2Fmultiarith.png)
## gsm8k聚类图
![gsm8k.png](demos%2Fgsm8k.png)

![](https://user-images.githubusercontent.com/22279212/194787183-a1f8dff8-a0ad-43a1-827f-819671503860.png)

![img.png](record%2Fimg.png)


## 运行try_cot.ipynb可以查看思维链示例

## 具体流程（这里以multiarith任务为例）：

首先建立一个包含训练数据的demo库:
```
python run_demo.py \
--task multiarith \
--pred_file log/multiarith_zero_shot_cot.log \
--demo_save_dir demos/multiarith
```
执行训练:
```
python run_inference.py \
--dataset multiarith \
--demo_path demos/multiarith \
--output_dir experiment/multiarith
```

