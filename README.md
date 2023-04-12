# Tucil 3 Stima IF2122 : A* & UCS shortest path finding

## Table of contents
* [Setup](#setup)
* [How to Use](#How-to-Use)
* [Author](#author)

## Setup

Clone this repo using the command below: 
git clone https://github.com/vanessrw/Tucil3_13521103_13521151.git

`
pip install networkx
pip install timit
pip install flask
`
jalankan `py web.py` pada terminal

## How to Use
masukan file input kedalam filder test. Berikur format file yang diterima (masukkan salah satu saja):
`10
-6.893080 107.608640 ParkirSipil 
-6.893225341866101 107.6104810985063 Kubus
-6.891197 107.608606 Cibe
-6.890610 107.610071 LabtekV
-6.889846277776866 107.61034392232239 Plawid
-6.892443757589303 107.61103842494695 AulaTimur
-6.890369 107.611841 GKUT
-6.890237 107.608724 GKUB
-6.888547699076628 107.61075509832881 Perpus
-6.887907780586676 107.61160336176233 CRCS
0 1 0 0 0 1 0 0 0 0
1 0 1 1 0 0 0 0 0 0
0 1 0 0 1 0 0 0 0 0
0 1 0 0 1 0 1 0 0 0
0 0 1 1 0 0 0 1 0 0
1 0 0 0 0 0 1 1 1 0
0 0 0 1 0 1 0 1 0 0
0 0 0 0 1 1 1 0 0 1
0 0 0 0 0 1 0 0 0 1
0 0 0 0 0 0 0 1 1 0
`
atau 
`
A,B,C,D,E,F,G,H
0  2  0  0  0  0  3  0
2  0  7  0  0  0  1  0
0  7  0  1  0  0  0  4
0  0  1  0  4  0  0  0
0  0  0  4  0  5  0  0
0  0  0  0  5  0  6  0
3  1  0  0  0  6  0  0
0  0  4  0  0  0  0  0
`

## Author
* Aulia Mey Diva Annandya - 13521103
* Vanessa Rebecca Wiyono - 13521151
