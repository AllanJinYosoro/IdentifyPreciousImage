# IdentifyPreciousImage
## ClusterImage
==ToDo==
## FixMatch
This is forked from an unofficial PyTorch implementation of [FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence](https://arxiv.org/abs/2001.07685).
The official Tensorflow implementation is [here](https://github.com/google-research/fixmatch).

### dataset
labeled_train in ./data/lb
unlabeled_train in ./data/ulb
test in ./data/test

### suggested command line

```
# python Mytrain.py --num-workers 4 --dataset PhotoGraph --batch-size 9 --num-labeled 45 --eval-step 1024 --total-steps 204800 --arch wideresnet  --lr 0.03 --expand-labels --seed 5  --out results/202311281553

python FixMatch/Mypredict.py --num-workers 4 --dataset PhotoGraph --batch-size 9 --num-labeled 45 --eval-step 1024 --total-steps 102400 --arch wideresnet  --lr 0.03 --expand-labels --seed 5  --out results/202311211517FXY --predict_model_path results\checkpoint.pth.tar --predict_data_path ./results/test

python __Mypredict.py --num-workers 4 --dataset PhotoGraph --batch-size 9 --num-labeled 45 --eval-step 1024 --total-steps 102400 --arch wideresnet  --lr 0.03 --expand-labels --seed 5  --out results/202311211517FXY --predict_model_path results\model_best.pth.tar --predict_data_path ./results/test
```
### Requirements
- python 3.6+
- torch 1.4
- torchvision 0.5
- tensorboard
- numpy
- tqdm
- apex (optional)


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
