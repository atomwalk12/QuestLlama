async function mineTwoDirtBlocks(bot) {
  let dirtCount = 0;
  while (dirtCount < 2) {
    const direction = new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1);
    const dirtBlock = await exploreUntil(bot, direction, 60, () => {
      return bot.findBlock({
        matching: mcData.blocksByName.dirt.id,
        maxDistance: 32
      });
    });
    if (dirtBlock) {
      bot.chat("Dirt block found. Mining...");
      await mineBlock(bot, "dirt", 1);
      dirtCount++;
      bot.chat(`Mined ${dirtCount} dirt blocks.`);
    } else {
      bot.chat("Could not find a dirt block within range.");
    }
  }
}