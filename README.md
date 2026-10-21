# RPack

Recipes I am missing in vanilla Minecraft, packed as a Fabric mod.
Drop the jar into your `mods` folder and the recipes are active in every
world, with no need to copy a datapack into each save.

Requires **Fabric API**. Builds for Minecraft **26.2** and **26.3**.

## Recipes

**Crafting table**

- 24 slabs from 3 logs, 16 stairs from 6 logs (every wood type, incl. nether stems; poplar on 26.3)
- 16 sticks from 2 logs, 4 chests from 8 logs (any log)
- 4 quartz from 1 quartz block, 4 clay balls from 1 clay block
- 4 string from 1 wool, 4 leather from 1 saddle
- Chainmail helmet, chestplate, leggings and boots from iron chains
- Spawner (iron bars), lodestone (stone + quartz)
- Grass block, mycelium, podzol, crimson and warped nylium
- Dispenser from dropper + bow, coal block from 9 charcoal
- 4 cobwebs from 4 string + slimeball, slime spawn egg from warped roots + egg
- Pointed dripstone from 5 dripstone blocks
- 7 crying obsidian from 7 obsidian + ghast tear + lava bucket

**Smithing table** (no template needed)

- 4 black dye from 2 charcoal
- Iron chain from 2 iron nuggets
- Chipped anvil + nugget → anvil; damaged anvil + nugget → chipped anvil; damaged anvil + ingot → anvil

**Furnace and blast furnace**

- Iron and gold tools, weapons and armor give back the ingots they cost:
  sword 2, pickaxe 3, axe 3, hoe 2, shovel 1, spear 1,
  helmet 5, chestplate 8, leggings 7, boots 4
- Chainmail armor gives back one iron ingot per chain (5/8/7/4)
- Bucket back to 3 iron ingots
- Horse armor back to 8 of its material (leather, iron, gold, diamond)
- Dripstone block from smooth basalt

Enchantments are lost and damage does not matter. RPack replaces the
vanilla "nugget from smelting/blasting" recipes so they only cover nautilus
armor (which is not craftable); otherwise two furnace recipes would compete
for the same input.

## Building

    ./build.sh

creates `build/rpack-<version>+26.2.jar` and `build/rpack-<version>+26.3.jar`.
`src/common` holds the recipes shared by both versions, `src/26.2` and
`src/26.3` the rest (blast furnace times are stored differently since 26.3,
and poplar only exists in 26.3). `tools/gen.py` generated the JSON once and
is kept for reference. `legacy/` is the original datapack 1.3.1.

## How this mod is made

Version 2.0 is written by Claude AI: the recipes, the build script and the descriptions.
Konitor decides what goes in and tests every version in game.
The icon is hand-made by Konitor in GIMP; no images are AI-generated.
