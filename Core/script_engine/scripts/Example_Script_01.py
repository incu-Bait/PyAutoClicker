# =====================
# Simple Counting Loop
# =====================
pyscript.log("Counting to 8")
count = 0
while count < 8 and pyscript.is_running():
    count += 1
    print(f"  Count: {count}")
    pyscript.wait(0.5)
pyscript.log("Finished counting!")