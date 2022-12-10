

def FMeasure(P, R):
    nom = 2 * P * R
    denom = P + R
    ans = nom / denom
    return ans


PT = [1,1,1,0.9,0.9]
RT = [0.078,0.078,0.078,0.070,0.070]

PB = [0.6,0.5,0.4,0.7,0.5]
RB = [0.039,0.032,0.026,0.045,0.074]


for i in range(0,5):
    ans = FMeasure(PT[i], RT[i])
    print(round(ans,3))

print()

for i in range(0,5):
    ans = FMeasure(PB[i], RB[i])
    print(round(ans,3))