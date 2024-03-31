async function equipIronSword(bot) {
  // Find the iron sword in the bot's inventory
  const ironSword = bot.inventory.findInventoryItem(mcData.itemsByName["iron_sword"].id);

  // Equip the iron sword in the main hand
  if (ironSword) {
    await bot.equip(ironSword, "hand");
    bot.chat("Iron sword equipped.");
  } else {
    bot.chat("No iron sword found in inventory.");
  }
}