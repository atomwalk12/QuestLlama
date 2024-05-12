async function mineThreeCopperOres(bot) {
  let copperOreCount = 0;
  while (copperOreCount < 3) {
    const direction = new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1);
    const copperOreBlock = await exploreUntil(bot, direction, 60, () => {
      return bot.findBlock({
        matching: mcData.blocksByName.copper_ore.id,
        maxDistance: 32
      });
    });
    if (copperOreBlock) {
      bot.chat("Copper ore found. Mining...");
      await mineBlock(bot, "copper_ore", 1);
      copperOreCount++;
      bot.chat(`Mined ${copperOreCount} copper ores.`);
    } else {
      bot.chat("Could not find a copper ore within range.");
    }
  }
}