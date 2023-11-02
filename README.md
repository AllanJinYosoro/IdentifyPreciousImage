# FixMatch
This is an unofficial PyTorch implementation of [FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence](https://arxiv.org/abs/2001.07685).
The official Tensorflow implementation is [here](https://github.com/google-research/fixmatch).

This code is only available in FixMatch (RandAugment).

## Results

### CIFAR10
| #Labels | 40 | 250 | 4000 |
|:---:|:---:|:---:|:---:|
| Paper (RA) | 86.19 ± 3.37 | 94.93 ± 0.65 | 95.74 ± 0.05 |
| This code | 93.60 | 95.31 | 95.77 |
| Acc. curve | [link](https://tensorboard.dev/experiment/YcLQA52kQ1KZIgND8bGijw/) | [link](https://tensorboard.dev/experiment/GN36hbbRTDaBPy7z8alE1A/) | [link](https://tensorboard.dev/experiment/5flaQd1WQyS727hZ70ebbA/) |

\* November 2020. Retested after fixing EMA issues.
### CIFAR100
| #Labels | 400 | 2500 | 10000 |
|:---:|:---:|:---:|:---:|
| Paper (RA) | 51.15 ± 1.75 | 71.71 ± 0.11 | 77.40 ± 0.12 |
| This code | 57.50 | 72.93 | 78.12 |
| Acc. curve | [link](https://tensorboard.dev/experiment/y4Mmz3hRTQm6rHDlyeso4Q/) | [link](https://tensorboard.dev/experiment/mY3UExn5RpOanO1Hx1vOxg/) | [link](https://tensorboard.dev/experiment/EDb13xzJTWu5leEyVf2qfQ/) |

\* Training using the following options `--amp --opt_level O2 --wdecay 0.001`

## Usage

### Train
Train the model by 4000 labeled data of CIFAR-10 dataset:

```
python train.py --dataset cifar10 --num-labeled 4000 --arch wideresnet --batch-size 64 --lr 0.03 --expand-labels --seed 5 --out results/cifar10@4000.5
# python Mytrain.py --num-workers 4 --dataset PhotoGraph --batch-size 9 --num-labeled 45 --eval-step 1024  --arch wideresnet --batch-size 64 --lr 0.03 --expand-labels --seed 5 --out results/Mytest
```

Train the model by 10000 labeled data of CIFAR-100 dataset by using DistributedDataParallel:
```
python -m torch.distributed.launch --nproc_per_node 4 ./train.py --dataset cifar100 --num-labeled 10000 --arch wideresnet --batch-size 16 --lr 0.03 --wdecay 0.001 --expand-labels --seed 5 --out results/cifar100@10000
```

### Monitoring training progress
```
tensorboard --logdir=<your out_dir>
```

## Requirements
- python 3.6+
- torch 1.4
- torchvision 0.5
- tensorboard
- numpy
- tqdm
- apex (optional)

## My other implementations
- [Meta Pseudo Labels](https://github.com/kekmodel/MPL-pytorch)
- [UDA for images](https://github.com/kekmodel/UDA-pytorch)


## References
- [Official TensorFlow implementation of FixMatch](https://github.com/google-research/fixmatch)
- [Unofficial PyTorch implementation of MixMatch](https://github.com/YU1ut/MixMatch-pytorch)
- [Unofficial PyTorch Reimplementation of RandAugment](https://github.com/ildoonet/pytorch-randaugment)
- [PyTorch image models](https://github.com/rwightman/pytorch-image-models)

## Citations
```
@misc{jd2020fixmatch,
  author = {Jungdae Kim},
  title = {PyTorch implementation of FixMatch},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/kekmodel/FixMatch-pytorch}}
}
```
