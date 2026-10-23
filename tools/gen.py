#!/usr/bin/env python3
"""One-off: write the RPack recipes for Minecraft 26.2 / 26.3 (Fabric)."""
import json, os, sys

OUT, VANILLA, VER = sys.argv[1], sys.argv[2], sys.argv[3]  # repo root, vanilla recipe dir, 26.2|26.3
NS = "konitor"
COMMON = os.path.join(OUT, "src/common/data", NS, "recipe")
REC = os.path.join(OUT, "src", VER, "data", NS, "recipe")
VREC = os.path.join(OUT, "src", VER, "data/minecraft/recipe")
for d in (COMMON, REC, VREC):
    os.makedirs(d, exist_ok=True)

def mc(x):
    if ":" in x:
        return x
    return "#minecraft:" + x[1:] if x.startswith("#") else "minecraft:" + x

def res(item, count=1):
    r = {"id": mc(item)}
    if count != 1:
        r["count"] = count
    return r

def write(d, name, data):
    with open(os.path.join(d, name + ".json"), "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

def shaped(name, pattern, key, item, count=1, category="misc"):
    data = {"type": "minecraft:crafting_shaped", "category": category,
            "pattern": pattern, "key": {k: mc(v) for k, v in key.items()},
            "result": res(item, count)}
    write(COMMON if not name.endswith(("poplar_slabs", "poplar_stairs")) else REC, name, data)

def shapeless(name, ingr, item, count=1):
    write(COMMON, name, {"type": "minecraft:crafting_shapeless", "category": "misc",
                      "ingredients": [mc(i) for i in ingr], "result": res(item, count)})

def cooking(name, ingr, item, count, xp, time):
    # 26.2 blasting recipes store the real (halved) time; since 26.3 they store
    # the furnace time and the blast furnace itself runs twice as fast
    blast = time if VER != "26.2" else time // 2
    for typ, t, suffix, d in (("smelting", time, "", COMMON), ("blasting", blast, "_blasting", REC)):
        write(d, name + suffix, {"type": "minecraft:" + typ, "category": "misc",
              "ingredient": mc(ingr), "result": res(item, count),
              "experience": xp, "cookingtime": t})

def smithing(name, base, addition, item, count=1):
    write(COMMON, name, {"type": "minecraft:smithing_transform", "base": mc(base),
                      "addition": mc(addition), "result": res(item, count)})

# --- wood: 24 slabs from 3 logs, 16 stairs from 6 logs
woods = [("oak", "#oak_logs"), ("spruce", "#spruce_logs"), ("birch", "#birch_logs"),
         ("jungle", "#jungle_logs"), ("acacia", "#acacia_logs"), ("dark_oak", "#dark_oak_logs"),
         ("mangrove", "#mangrove_logs"), ("cherry", "#cherry_logs"), ("pale_oak", "#pale_oak_logs"),
         ("crimson", "#crimson_stems"), ("warped", "#warped_stems")]
if VER != "26.2":
    woods.append(("poplar", "#poplar_logs"))  # added in 26.3
for w, tag in woods:
    shaped(f"24{w}_slabs", ["###"], {"#": tag}, f"{w}_slab", 24, "building")
    shaped(f"16{w}_stairs", ["#  ", "## ", "###"], {"#": tag}, f"{w}_stairs", 16, "building")

# --- crafting table
shaped("16sticks", ["#", "#"], {"#": "#logs"}, "stick", 16)
shaped("4chests", ["###", "# #", "###"], {"#": "#logs"}, "chest", 4)
shapeless("4quartz", ["quartz_block"], "quartz", 4)
shapeless("4strings", ["#wool"], "string", 4)
shapeless("4clayfromclay", ["clay"], "clay_ball", 4)
shapeless("4leather_from_saddle", ["saddle"], "leather", 4)
shaped("chainmail_helmet", ["###", "# #"], {"#": "iron_chain"}, "chainmail_helmet", 1, "equipment")
shaped("chainmail_chestplate", ["# #", "###", "###"], {"#": "iron_chain"}, "chainmail_chestplate", 1, "equipment")
shaped("chainmail_leggings", ["###", "# #", "# #"], {"#": "iron_chain"}, "chainmail_leggings", 1, "equipment")
shaped("chainmail_boots", ["# #", "# #"], {"#": "iron_chain"}, "chainmail_boots", 1, "equipment")
shaped("spawner", ["###", "###", "###"], {"#": "iron_bars"}, "spawner")
shaped("lodestone", ["###", "#Q#", "###"], {"#": "stone", "Q": "quartz"}, "lodestone")
shaped("grass_block", ["#", "D"], {"#": "short_grass", "D": "dirt"}, "grass_block", 1, "building")
shaped("mycelium_block", ["#", "D"], {"#": "brown_mushroom", "D": "dirt"}, "mycelium", 1, "building")
shaped("podzol_block", ["#", "D"], {"#": "fern", "D": "dirt"}, "podzol", 1, "building")
shaped("crimson_nylium", ["#", "N"], {"#": "crimson_roots", "N": "netherrack"}, "crimson_nylium", 1, "building")
shaped("warped_nylium", ["#", "N"], {"#": "warped_roots", "N": "netherrack"}, "warped_nylium", 1, "building")
shaped("disp_from_dropper", ["#", "D"], {"#": "bow", "D": "dropper"}, "dispenser", 1, "redstone")
shaped("coalblock", ["###", "###", "###"], {"#": "charcoal"}, "coal_block", 1, "building")
shaped("cobweb", [" # ", "#S#", " # "], {"#": "string", "S": "slime_ball"}, "cobweb", 4)
shaped("slime_spawn_egg", ["###", "#E#", "###"], {"#": "warped_roots", "E": "egg"}, "slime_spawn_egg")
shaped("pointed_dripstone", ["###", " # ", " # "], {"#": "dripstone_block"}, "pointed_dripstone", 1, "building")
shaped("crying_obsidian", ["#L#", "#G#", "###"], {"#": "obsidian", "L": "lava_bucket", "G": "ghast_tear"}, "crying_obsidian", 7, "building")

# --- smithing table (no template needed)
smithing("4blackdye", "charcoal", "charcoal", "black_dye", 4)
smithing("4blackdye_from_coal", "coal", "coal", "black_dye", 4)
smithing("chain-smithing", "iron_nugget", "iron_nugget", "iron_chain")
smithing("repair-chipped-anvil", "chipped_anvil", "iron_nugget", "anvil")
smithing("repair-damaged-anvil1", "damaged_anvil", "iron_nugget", "chipped_anvil")
smithing("repair-damaged-anvil2", "damaged_anvil", "iron_ingot", "anvil")

# --- furnace and blast furnace: tools and armor give back the ingots they cost
recycle = []
def recycle_to(name, ingr, item, n):
    cooking(name, ingr, item, n, n / 10, 100 + n * 10)
    recycle.append(mc(ingr))
for metal, ingot, prefix in (("iron", "iron_ingot", "iron"), ("gold", "gold_ingot", "golden")):
    for piece, n in (("sword", 2), ("boots", 4), ("helmet", 5), ("leggings", 7), ("chestplate", 8),
                     ("pickaxe", 3), ("axe", 3), ("hoe", 2), ("shovel", 1), ("spear", 1)):
        recycle_to(f"{n}{metal}_from_{piece}", f"{prefix}_{piece}", ingot, n)
# chainmail is crafted from iron chains here: one ingot back per chain
for piece, n in (("boots", 4), ("helmet", 5), ("leggings", 7), ("chestplate", 8)):
    recycle_to(f"{n}iron_from_chainmail_{piece}", f"chainmail_{piece}", "iron_ingot", n)
cooking("3iron_from_bucket", "bucket", "iron_ingot", 3, 0.3, 130)
for armor, item in (("iron_horse_armor", "iron_ingot"), ("golden_horse_armor", "gold_ingot"),
                    ("diamond_horse_armor", "diamond"), ("leather_horse_armor", "leather")):
    cooking(armor.replace("golden", "gold").replace("diamond", "dia"), armor, item, 8, 0.8, 180)
    recycle.append(mc(armor))
cooking("dripstone", "smooth_basalt", "dripstone_block", 1, 0.1, 200)

# --- vanilla nugget recipes minus the items RPack recycles into ingots,
# otherwise two furnace recipes compete for the same input (only nautilus armor is left)
for metal in ("iron", "gold"):
    for typ in ("smelting", "blasting"):
        vanilla = json.load(open(os.path.join(VANILLA, f"{metal}_nugget_from_{typ}.json")))
        vanilla["ingredient"] = [i for i in vanilla["ingredient"] if i not in recycle]
        write(VREC, f"{metal}_nugget_from_{typ}", vanilla)

print(VER, len(os.listdir(COMMON)), "common,", len(os.listdir(REC)), "version-specific,",
      len(os.listdir(VREC)), "vanilla overrides")
