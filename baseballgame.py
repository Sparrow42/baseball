# -*- coding: utf-8 -*-
"""
Created on Fri May 24 00:59:35 2019

@author: Tshr Ban

2019/05/24: project start.
投手のみ、打者のみで実装する。
1回3アウト取った時点で終了する。

2019/05/25: 更新
カウントクラスの追加。カウントが上限に達したときの場合も追加（未検証）
ベースクラスの実装。追加できるところまではいったが、各要素に足すところは未完。
ジャッジ関数がほぼ完成。
メイン関数の実装ができなかった。

2019\05\26:　更新
disp_frameの実装。
ジャッジ関数の修正。
Pitcherクラスに投げミスコースリストの実装。投げミスによるコースの変化を実装。確認済み。

<やること>
関数名がもやもやする。judgeはbatterと分けるべき。
コースをブロックではなく、座標で表現する。
"""

import random, math
#import numpy as np
import matplotlib.pyplot as plt

class Pitcher:
    type=["0"] #球種
    course=["0"] #投げるコース
    course_result=["0"] #投げミス含めたコース
    
class Count:
    ball=0
    strike=0
    out=0
    def count_filled(ball,strike,out):
        if ball >= 4:
            Base.filled.append(1)
            print("フォアボール\n",Base.filled)
        elif strike >= 3:
            out=out+1
            print("ストライクアウト\n",out)
        
        if out >= 3:
            print("スリーアウト　チェンジ！\n")
            return 0
               
class Base: #ベースのアルゴリズム(ベース数を配列に追加していき、新しく追加した数を既存の数に足してく)
    filled=[]


def judge(Count):
    swing_p=random.random() #この確率を色んなデータで算出したい（現状は１/2の確率で判定している）
    courseout_p=random.random()
    swing_estp=0.5 #スイングする確率
    courseout_estp=0.2 #コースを外す確率
    random_p = random.random() #代替可能なランダム確率（0～1）
    
    #スイングあり・アウトありー0.4でヒット・残りスト、スイングあり・アウトなしー0.25ヒット、残りスト、
    #スイングなし・アウトありー0.7スト・残りボール、スイングなし・アウトなしー1.0スト
    #振る確率、外す確率をつけたい
    if swing_p > swing_estp: #スイングした場合
        print("スイングしました。\n")
        if courseout_p < courseout_estp: #コース通りにいかなかった場合
            Pitcher.course_result[-1]=str(math.ceil(random.random()*8)+1) #ランダムで他のコースに変更
            print("コースアウトしました。\n")
            if random_p > 0.6: #6割ストライク、4割ヒット
                print("ストライク！")
                Count.strike=Count.strike+1
            else:
                print("ヒット！")
                Base.filled.append(1)
        else: #コース通りにいった場合
            if random_p > 0.8: #8割ストライク、2割ヒット
                print("ストライク！")
                Count.strike=Count.strike+1
            else:
                print("ヒット！")
                Base.filled.append(1)
                #ヒットした場合の変数作る。（走塁の実装も）
    else: #スイングしなかった場合(現状はストライク判定のみ)
        print("スイングしませんでした。\n")
        if courseout_p < courseout_estp: #コース通りにいかなかった場合
            Pitcher.course_result[-1]=str(math.ceil(random.random()*8)+1) #ランダムで他のコースに変更
            print("コースアウト\n")
            if random_p > 0.8: #8割ストライク、2割ボール(投球内容としてはボールのコースにはいかないです)
                print("ストライク！")
                Count.strike=Count.strike+1
            else:
                print("ボール！")
                Count.ball=Count.ball+1
        else: #コース通りにいった場合
            print("ストライク！")
            Count.strike=Count.strike+1
        
    print("(スイング, コースアウト, ランダム) = ",(swing_p, courseout_p, random_p))
    return Count


dic={"st":"ストレート","c":"カーブ","sp":"スプリット"}

strike_size = 3 #ストライクゾーンの辺(現状は2,3のみ可能)
#strike_num = strike_size**2

#投手操作

def disp_frame(Pitcher,init=0):#ストライクゾーン出力 & init:デフォルトで投げたコース出力（0以外で数字のみ）
    print("-"+"----"*strike_size)
    for i in range(strike_size):
        for j in range(strike_size):
            #print(int(Pitcher.course[-1]),j+strike_size*(strike_size-i-1)+1,init)
            #球種・コース選択後の場合は、結果を出力する。type,courseの最後の配列を出力する。
            #コース通りにいかなかった場合に対応していない。1回表が終わったらPitcherは初期化する。
            if int(Pitcher.course_result[-1])==j+strike_size*(strike_size-i-1)+1 and init==0:
                print("|",Pitcher.type[-1],"",end="")
                #print("complete")
            else:
                print("|",j+strike_size*(strike_size-i-1)+1,"", end="")
        print("|\n-"+"----"*strike_size)

disp_frame(Pitcher,init=1)

#print(dic)
print("球種を選択してください。", "{}；".format(dic)) #キーと値をそれぞれ出力したいができない
t = input() #文字列として入力される
Pitcher.type.append(t)
print(Pitcher.type, end="")

c=input("投げるコースを選択してください。（１～９）；")
Pitcher.course.append(c)
Pitcher.course_result.append(c)
print("予定コース；",Pitcher.course)

judge(Count)
print("コースアウト時；",Pitcher.course_result)

disp_frame(Pitcher)

print("カウント；",Count.ball,"ボール,",Count.strike,"ストライク,",Count.out,"アウト\n")

