async function mineRoseBushes(bot) {
  let roseBushCount = 0;
  while (roseBushCount < 10) {
    const direction = new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1);
    const roseBushBlock = await exploreUntil(bot, direction, 60, () => {
      return bot.findBlock({
        matching: block => block.name === "rose_bush",
        maxDistance: 32
      });
    });
    if (roseBushBlock) {
      bot.chat("Rose bush found. Mining...");
      await mineBlock(bot, "rose_bush", 1);
      roseBushCount++;
      bot.chat(`Mined ${roseBushCount} rose bushes.`);
    } else {
      bot.chat("Could not find a rose bush within range.");
    }
  }
}