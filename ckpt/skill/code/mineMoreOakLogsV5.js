async function mineMoreOakLogs(bot) {
  // Check if there's an axe in the inventory
  let axeCount = bot.inventory.count(mcData.itemsByName.wooden_pickaxe.id);
  if (axeCount < 1) {
    // Place a crafting table nearby
    await placeItem(bot, "crafting_table", bot.entity.position.offset(1, 0, 0));
    // Craft a wooden pickaxe using oak logs
    await mineBlock(bot, "oak_log", 3);
    await craftItem(bot, "wooden_pickaxe", 1);
  }

  // Explore until an oak tree is found
  let oakTreeBlock;
  while (!oakTreeBlock) {
    const direction = new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1);
    oakTreeBlock = await exploreUntil(bot, direction, 60, () => {
      return bot.findBlock({
        matching: block => block.name === "oak_log",
        maxDistance: 32
      });
    });
    if (oakTreeBlock) {
      bot.chat("Oak tree found. Mining...");
      // Mine 3 more oak logs
      await mineBlock(bot, "oak_log", 3);
      bot.chat("Mined 3 more oak logs.");
    } else {
      bot.chat("Could not find an oak tree within range.");
    }
  }
}