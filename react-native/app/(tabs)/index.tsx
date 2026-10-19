import { LinearGradient } from 'expo-linear-gradient';
import React, { useState } from 'react';
import {
  ActivityIndicator,
  Image,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
} from 'react-native';

// Defina EXPO_PUBLIC_API_URL (ex.: http://192.168.0.10:8000) em um arquivo .env.
const API_URL = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000';

export default function HomeScreen() {
  const [nome1, setNome1] = useState('');
  const [nome2, setNome2] = useState('');
  const [resultado, setResultado] = useState('');
  const [erro, setErro] = useState('');
  const [carregando, setCarregando] = useState(false);

  const preverBatalha = async () => {
    setResultado('');
    setErro('');
    if (!nome1.trim() || !nome2.trim()) {
      setErro('Preencha os dois nomes de pokémon.');
      return;
    }

    setCarregando(true);
    try {
      const response = await fetch(`${API_URL}/prever`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome1, nome2 }),
      });
      const data = await response.json();
      if (response.ok) {
        setResultado(`🏆 ${data.vencedor} (${(data.confianca * 100).toFixed(1)}% de confiança)`);
      } else {
        setErro(typeof data.detail === 'string' ? data.detail : 'Erro na resposta da API.');
      }
    } catch {
      setErro('Não foi possível conectar à API.');
    } finally {
      setCarregando(false);
    }
  };

  return (
    <LinearGradient
      colors={['#1a1a1a', '#2e2e2e', '#3a3a3a']}
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 1 }}
      style={styles.gradientBackground}>
      <KeyboardAvoidingView
        style={styles.gradientBackground}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <ScrollView contentContainerStyle={styles.scroll}>
          <Image
            source={require('../../assets/images/pokemon.jpg')}
            style={styles.topImage}
            resizeMode="contain"
          />
          <Text style={styles.title}>Batalha Pokémon</Text>
          <TextInput
            style={styles.input}
            placeholder="Digite o nome do primeiro pokémon"
            placeholderTextColor="#999"
            onChangeText={setNome1}
            value={nome1}
          />
          <TextInput
            style={styles.input}
            placeholder="Digite o nome do segundo pokémon"
            placeholderTextColor="#999"
            onChangeText={setNome2}
            value={nome2}
          />
          <LinearGradient
            colors={['#2e2e2e', '#444444', '#666666']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={styles.batalha}>
            <TouchableOpacity onPress={preverBatalha} disabled={carregando}>
              {carregando ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.batalhaText}>Iniciar batalha</Text>
              )}
            </TouchableOpacity>
          </LinearGradient>
          {resultado ? <Text style={styles.result}>{resultado}</Text> : null}
          {erro ? <Text style={styles.error}>{erro}</Text> : null}
        </ScrollView>
      </KeyboardAvoidingView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  gradientBackground: { flex: 1 },
  scroll: { padding: 20, alignItems: 'center', justifyContent: 'center' },
  topImage: { width: '100%', height: 250, marginBottom: 30 },
  title: { fontSize: 26, fontWeight: 'bold', textAlign: 'center', marginBottom: 30, color: '#fff' },
  input: {
    width: '100%',
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#aaa',
    borderRadius: 8,
    padding: 12,
    marginBottom: 15,
  },
  batalha: { width: '100%', padding: 15, borderRadius: 8, alignItems: 'center' },
  batalhaText: { color: '#fff', fontWeight: 'bold' },
  result: { marginTop: 20, fontSize: 22, textAlign: 'center', color: '#fff' },
  error: { marginTop: 20, fontSize: 16, textAlign: 'center', color: '#ff8080' },
});
