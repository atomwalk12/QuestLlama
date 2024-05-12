async function killChicken(bot) {
  // Check if we have a wooden pickaxe in our inventory. If not, craft one.
  let woodenPickaxeCount = bot.inventory.count(mcData.itemsByName.wooden_pickaxe.id);
  if (woodenPickaxeCount < 1) {
    await craftWoodenPickaxe(bot);
  }

  // Equip the wooden pickaxe
  const woodenPickaxe = bot.inventory.findInventoryItem(mcData.itemsByName.wooden_pickaxe.id);
  await bot.equip(woodenPickaxe, "hand");

  // Explore until we find a chicken within a range of 32 blocks.
  let chicken;
  while (!chicken) {
    const direction = new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1);
    chicken = await exploreUntil(bot, direction, 60, () => {
      return bot.nearestEntity(entity => entity.name === "chicken" && entity.position.distanceTo(bot.entity.position) < 32);
    });
    if (chicken) {
      bot.chat("Chicken found.");
    } else {
      bot.chat("Could not find a chicken within range.");
    }
  }

  // Kill the chicken using the equipped wooden pickaxe.
  await killMob(bot, "chicken", 300);
  bot.chat("1 chicken killed.");
}