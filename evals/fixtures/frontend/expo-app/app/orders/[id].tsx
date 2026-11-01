import { View, Text } from "react-native";
import { useLocalSearchParams } from "expo-router";
import { useOrder } from "../../data/orders";

export default function OrderScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const order = useOrder(id); // undefined when no order has this id

  return (
    <View>
      <Text accessibilityRole="header">{order.reference}</Text>
      <Text>{order.status}</Text>
    </View>
  );
}
