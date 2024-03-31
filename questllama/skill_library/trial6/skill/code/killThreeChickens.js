async function killThreeChickens(bot) {
  for (let i = 0; i < 3; i++) {
    // Explore until finding a chicken
    const chicken = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
      const chicken = bot.nearestEntity(entity => {
        return entity.name === "chicken" && entity.position.distanceTo(bot.entity.position) < 32;
      });
      return chicken;
    });
    if (chicken) {
      // Kill the chicken
      await killMob(bot, "chicken", 300);
      bot.chat(`Killed chicken ${i + 1}/3.`);
    } else {
      bot.chat("Could not find enough chickens.");
      break;
    }
  }
}