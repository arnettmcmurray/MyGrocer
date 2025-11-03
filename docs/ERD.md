# MyGrocer MVP ERD (Phase 1)

Entities:
- users
- categories (user_id → users.id)
- source_items (user_id → users.id, category_id → categories.id nullable)
- pantry_items (user_id → users.id, source_item_id → source_items.id)
- grocery_lists (user_id → users.id, is_active bool)
- grocery_list_items (list_id → grocery_lists.id, source_item_id → source_items.id)

Rules:
- Categories and SourceItems are user-scoped.
- Single active GroceryList per user enforced in app logic.
- PantryItem expiration_date optional.
