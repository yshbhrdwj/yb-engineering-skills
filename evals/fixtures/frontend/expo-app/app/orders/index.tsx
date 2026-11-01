import { FlatList } from "react-native";
import { router } from "expo-router";
import { ListRow } from "../../ListRow";
import { useOrders } from "../../data/orders";

export default function OrdersScreen() {
  const orders = useOrders();
  return (
    <FlatList
      data={orders}
      keyExtractor={(order) => order.id}
      renderItem={({ item }) => (
        // Navigation refactor (PR 88): was router.push.
        <ListRow title={item.reference} subtitle={item.status} onPress={() => router.replace(`/orders/${item.id}`)} />
      )}
    />
  );
}
