# RoTBench
## RoTBench: A Multi-Level Benchmark for Evaluating the Robustness of Large Language Models in Tool Learning

> Data for paper [RoTBench: A Multi-Level Benchmark for Evaluating the Robustness of Large Language Models in Tool Learning](https://arxiv.org/abs/2401.08326)

Junjie Ye

jjye23@m.fudan.edu.cn

Jan. 16, 2024

## Introduction
Tool learning has generated widespread interest as a vital means of interaction between Large Language Models (LLMs) and the physical world. Current research predominantly emphasizes LLMs' capacity to utilize tools in well-structured environments while overlooking their stability when confronted with the inevitable noise of the real world.
To bridge this gap, we introduce \emph{RoTBench}, a multi-level benchmark for evaluating the robustness of LLMs in tool learning. RoTBench consists of five external environments, each featuring varying levels of noise (i.e., Clean, Slight, Medium, Heavy, and Union), providing an in-depth analysis of the model's resilience across three critical phases: tool selection, parameter identification, and content filling.
Experiments involving six widely-used models underscore the urgent necessity for enhancing the robustness of LLMs in tool learning.
For instance, the performance of GPT-4 even drops significantly from 78.10 to 55.24 when there is no substantial change in manual accuracy.
More surprisingly, the noise correction capability inherent in the GPT family paradoxically impedes its adaptability in the face of mild noise.
In light of these findings, we propose RoTTuning, a strategy that enriches the diversity of training environments to bolster the robustness of LLMs in tool learning.

<div>
<center>
<img src=Figures/RoTBench.png>
</div>

## What's New
- **[2024.02.03]** The code is released. The instruction for evaluation is on its way.
- **[2024.01.17]** The data is released.
- **[2024.01.16]** Paper available on [Arxiv](https://arxiv.org/abs/2401.08326).


## Requirement
- Run the command to install the packages required.
    ```bash
    pip install -r requirements.txt
    ```


## Main Result
As tool learning involves multiple turns of interaction between LLMs and the environment, with intricate intermediate trajectories that cannot be easily compared, our emphasis lies on evaluating the robustness of their performance in a single turn of interaction. Specifically, we evaluate the performance of various LLMs during their initial use of the tool.

<div>
<center>
<img src=Figures/result.png>
</div>


## RoTTuning

In light of the experimental findings, it is evident that enhancing the robustness of LLMs in tool learning is imperative. To tackle this issue, we introduce RoTTuning, a novel approach aimed at bolstering the robustness of LLMs in tool learning through increased environmental diversity. Subsequent sections will provide a detailed explanation of this approach.

<div>
<center>
<img src=Figures/RoTTuning.png>
</div>

## Citation
If you find this project useful in your research, please cite:
```
@misc{ye2024rotbench,
      title={RoTBench: A Multi-Level Benchmark for Evaluating the Robustness of Large Language Models in Tool Learning}, 
      author={Junjie Ye and Yilong Wu and Songyang Gao and Sixian Li and Guanyu Li and Xiaoran Fan and Qi Zhang and Tao Gui and Xuanjing Huang},
      year={2024},
      eprint={2401.08326},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
