async function mineThreeLilacs(bot) {
  let lilacCount = 0;
  while (lilacCount < 3) {
    const direction = new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1);
    const lilacBlock = await exploreUntil(bot, direction, 60, () => {
      return bot.findBlock({
        matching: block => block.name === "lilac",
        maxDistance: 32
      });
    });
    if (lilacBlock) {
      bot.chat("Lilac found. Mining...");
      await mineBlock(bot, "lilac", 1);
      lilacCount++;
      bot.chat(`Mined ${lilacCount} lilacs.`);
    } else {
      bot.chat("Could not find a lilac within range.");
    }
  }
}