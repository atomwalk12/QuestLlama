async function obtainOakLog(bot) {
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
      await mineBlock(bot, "oak_log", 1);
      bot.chat("Obtained an oak log.");
    } else {
      bot.chat("Could not find an oak tree within range.");
    }
  }
}