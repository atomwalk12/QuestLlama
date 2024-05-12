async function mineThreeCoalOres(bot) {
  let coalCount = bot.inventory.count(mcData.itemsByName.coal.id);
  while (coalCount < 3) {
    const direction = new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1);
    const coalOreBlock = await exploreUntil(bot, direction, 60, () => {
      return bot.findBlock({
        matching: mcData.blocksByName.coal_ore.id,
        maxDistance: 32
      });
    });
    if (coalOreBlock) {
      bot.chat("Coal ore found. Mining...");
      await mineBlock(bot, "coal_ore", 1);
      coalCount++;
      bot.chat(`Mined ${coalCount} coals.`);
    } else {
      bot.chat("Could not find a coal ore within range.");
    }
  }
}