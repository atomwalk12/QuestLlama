async function mineWoodLog(bot) {
  const woodLogNames = ["oak_log", "birch_log", "spruce_log", "jungle_log", "acacia_log", "dark_oak_log", "mangrove_log"];
  let woodLogBlock;

  // Explore until a wood log block is found
  while (!woodLogBlock) {
    const direction = new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1);
    woodLogBlock = await exploreUntil(bot, direction, 60, () => {
      return bot.findBlock({
        matching: block => woodLogNames.includes(block.name),
        maxDistance: 32
      });
    });
    if (woodLogBlock) {
      // Mine the found wood log block
      bot.chat("Wood log found. Mining...");
      await mineBlock(bot, woodLogBlock.name, 1);
      bot.chat("Wood log mined.");
    } else {
      bot.chat("Could not find a wood log within range.");
    }
  }
}