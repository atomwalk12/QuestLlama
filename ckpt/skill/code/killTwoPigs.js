async function killTwoPigs(bot) {
  // Equip a wooden pickaxe from the inventory
  const woodenPickaxe = bot.inventory.findInventoryItem(mcData.itemsByName.wooden_pickaxe.id);
  await bot.equip(woodenPickaxe, "hand");
  let pigCount = 0;
  while (pigCount < 2) {
    // Find the nearest pig using exploreUntil function
    let pig;
    while (!pig) {
      const direction = new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1);
      pig = await exploreUntil(bot, direction, 60, () => {
        return bot.nearestEntity(entity => entity.name === "pig" && entity.position.distanceTo(bot.entity.position) < 32);
      });
      if (pig) {
        bot.chat("Pig found.");
      } else {
        bot.chat("Could not find a pig within range.");
      }
    }

    // Kill the pig using the equipped wooden pickaxe with killMob function
    await killMob(bot, "pig", 300);
    bot.chat(`Killed ${pigCount + 1} pig.`);

    // Collect the dropped items after killing the pig
    await bot.pathfinder.goto(new GoalBlock(pig.position.x, pig.position.y, pig.position.z));
    bot.chat("Collected dropped items.");
    pigCount++;
  }
}