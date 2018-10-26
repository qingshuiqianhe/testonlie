# -*- coding: utf-8 -*-
import difflib
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

s1 = [[u'通信、 资源共享、 分布计算、 提高可靠性'], [u'非对称数字用户线'], [u'电信电平、负载容限、传输速率与传输距离'],
      [u'从数据发送开始到网络上最远的两个站之间信号传播时延的两倍止的时间区间'], [u'2.048 Mbps'],
      [u'LINK-STATE（链路状态）, V-D（距离向量）'], [u'简单邮件传输协议'], [u'25'], [u'TELNET'],
      [u'本地主机地址，本地端口号，协议，远程主机地址，远程端口号'],
      [u'由于节点要发送数据时，先侦听信道是否有载波，如果有，表示信道忙，则继续侦听，直至检测到空闲为止；'],
      [u'当一个数据帧从节点1向最远的节点传输过程中，如果有其他节点也正在发送数据，此时就发送冲突，冲突后的信号需要经过'
      u'冲突窗口时间后传回节点1，节点1就会检测到冲突，所以说如果有冲突则一定发生在冲突窗口内，如果在冲突窗口内没有'
       u'发生冲突，之后如果其他节点再要发送数据，就会侦听到信道忙，而不会发送数据，从不会再发送冲突。']
      ]
s2 = [[u'资源共享、 分布计算'], [u'对称数字用户线'], [u'电信电平、传输速率与传输距离'],
      [u'数据发送开始到最远的两个站之间信号时延的两倍止的时间'], [u'2.0 Mbps'],
      [u'LINK-STATE, （距离向量）'], [u'简单传输协议'], [u'25'], [u'TELNT'],
      [u'本地主机地址，协议，远程主机'],
      [u'由于节点要发送数据时，先侦听信道是否有载波，如果有，表示信道忙，则继续侦听，直至检测到空闲为止；'],
      [u'当一个数据帧从节点1向最远的节点传输过程中，如果有其他节点也正在发送数据，此时就发送冲突，冲突后的信号需要经过'
      u'冲突窗口时间后传回节点1，节点1就会检测到冲突，所以说如果有冲突则一定发生在冲突窗口内，如果在冲突窗口内没有'
       u'发生冲突，之后如果其他节点再要发送数据，就会侦听到信道忙，而不会发送数据，从不会再发送冲突。']
      ]

# for i in range(12):
#     ss = s1[i][0]
#     jj = s2[i][0]
#     # que_score = fuzz.partial_token_set_ratio(ss, jj, force_ascii=False, full_process=True)
#     # que_score = process.extract(jj, ss,  limit=12)
#     # process.dedupe(ss, threshold=11, scorer=fuzz.token_set_ratio)
#     que_score = difflib.SequenceMatcher(None, jj,  ss).ratio()
#     print que_score,'i=', i
#
# def getnext(a,next):
#     al = len(a)
#     next[0] = -1
#     k = -1
#     j = 0
#     while j < al-1:
#         if k == -1 or a[j] == a[k]:
#             j += 1
#             k += 1
#             next[j] = k
#         else:
#             k = next[k]
#
# def KmpSearch(a,b):
#     i = j = 0
#     al = len(a)
#     bl = len(b)
#     while i < al and j < bl:
#         if j == -1 or a[i] == b[j]:
#             i += 1
#             j += 1
#         else:
#             j = next[j]
#     if j == bl:
#         return i-j
#     else:
#         return -1
#
# a = '2.048'
# b = '2'
# next = [0]*len(b)
# getnext(b,next)
# t = KmpSearch(a,b)
# print(next)
# print(t)