async function mineIronOre(bot) {
  // Place a crafting table near the bot
  const craftingTablePosition = bot.entity.position.offset(1, 0, 0);
  await placeItem(bot, "crafting_table", craftingTablePosition);

  // Craft a stone pickaxe if not already in inventory
  let stonePickaxeCount = bot.inventory.count(mcData.itemsByName.stone_pickaxe.id);
  if (stonePickaxeCount < 1) {
    await craftItem(bot, "stone_pickaxe", 1);
    bot.chat("Crafted a stone pickaxe.");
  }

  // Explore until finding an iron ore block
  let ironOreFound = false;
  while (!ironOreFound) {
    const direction = new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1);
    const ironOreBlock = await exploreUntil(bot, direction, 60, () => {
      return bot.findBlock({
        matching: mcData.blocksByName.iron_ore.id,
        maxDistance: 32
      });
    });
    if (ironOreBlock) {
      bot.chat("Iron ore found. Mining...");
      await mineBlock(bot, "iron_ore", 1);
      ironOreFound = true;
      bot.chat("Mined 1 iron ore.");
    } else {
      bot.chat("Could not find an iron ore within range.");
    }
  }
}