import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn3_unweighted
import os
save_file = os.getcwd()
tests = ["LT", "DC", "TT"] # bend test should never take more than 1-2 days

Y = f"\x1b[32m √ \x1b[0m"
N = f"\x1b[31m X \x1b[0m"

tape_marker = lambda A, B, C: f"LT {A} DC {B} TT {C}: "

TT = int(input(tape_marker(N,N,Y)) )
DC = int(input(tape_marker(N,Y,N)))
LT = int(input(tape_marker(Y,N,N)))

LT_DC = int(input(tape_marker(Y,Y,N)))
DC_TT = int(input(tape_marker(N,Y,Y)))
LT_TT = int(input(tape_marker(Y,N,Y)))

LT_DC_TT = int(input(tape_marker(Y,Y,Y)))

total = TT + DC + LT + LT_DC + DC_TT + LT_TT + LT_DC_TT



percent = lambda value: f"({100 * value / total:.2f}%)"
venn_text = lambda x: f"{x}\n{percent(x)}"

v = venn3_unweighted(subsets = (LT,
								DC, 
								LT_DC, 
								TT, 
								LT_TT, 
								DC_TT, 
								LT_DC_TT), 
								set_labels = (f"Have only Leak Test\n(Tests Left: {DC+TT+DC_TT})", 
											  f"Have only DC Test\n(Tests Left: {LT+TT+LT_TT})", 
											  f"Have only Tension Test\n(Tests Left: {LT+DC+LT_DC})"),
								subset_label_formatter= venn_text
								)
v.get_patch_by_id("100").set_color("red")
v.get_patch_by_id("010").set_color("red")
v.get_patch_by_id("001").set_color("red")

v.get_patch_by_id("110").set_color("orange")
v.get_patch_by_id("011").set_color("orange")
v.get_patch_by_id("101").set_color("orange")

v.get_patch_by_id("111").set_color("green")
for text in v.set_labels:
    text.set_fontsize(8)
from datetime import datetime
today = datetime.strftime(datetime.now(), "%Y-%m-%d")

plt.title(f"Tube Room Tubes on {today}\n Total:{total}")
plt.savefig(f"{save_file}/tubepopulation.png")
plt.show()
