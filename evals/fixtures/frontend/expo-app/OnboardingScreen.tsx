import { useState } from "react";
import { View, Text, Switch, Button } from "react-native";
import { finishOnboarding } from "./session";

const STEPS = [
  { title: "Track every parcel", body: "Add a tracking number or forward a shipping email." },
  { title: "Know before the door", body: "Get one notification when a delivery is near." },
  { title: "You're set", body: "Choose whether we may send occasional product news." },
];

export default function OnboardingScreen() {
  const [step, setStep] = useState(0);
  const [marketingOptIn, setMarketingOptIn] = useState(false);

  return (
    <View style={{ flex: 1, padding: 20, paddingTop: 60, backgroundColor: "#fff" }}>
      <Text style={{ fontSize: 30, fontWeight: "bold" }} allowFontScaling={false}>
        {STEPS[step].title}
      </Text>
      <Text style={{ fontSize: 15, color: "#999", marginTop: 8 }}>{STEPS[step].body}</Text>

      {step === 2 && (
        <View style={{ flexDirection: "row", alignItems: "center", marginTop: 24 }}>
          <Switch value={marketingOptIn} onValueChange={setMarketingOptIn} accessibilityLabel="Send me product news" />
          <Text style={{ marginLeft: 8 }}>Send me product news</Text>
        </View>
      )}

      <View style={{ position: "absolute", bottom: 20, left: 20, right: 20 }}>
        <Button
          title={step < 2 ? "Next" : "Get started"}
          onPress={() => (step < 2 ? setStep(step + 1) : finishOnboarding({ marketingOptIn }))}
        />
        <Text onPress={() => finishOnboarding({ marketingOptIn: false })} style={{ textAlign: "center", marginTop: 12 }}>
          Skip
        </Text>
      </View>
    </View>
  );
}
