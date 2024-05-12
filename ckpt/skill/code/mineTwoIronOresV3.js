async function mineTwoIronOres(bot) {
  let ironOreCount = 0;
  while (ironOreCount < 2) {
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
      ironOreCount++;
      bot.chat(`Mined ${ironOreCount} iron ores.`);
    } else {
      bot.chat("Could not find an iron ore within range.");
    }
  }
}