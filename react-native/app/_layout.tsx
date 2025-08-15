import { PlatformPressable } from "@react-navigation/elements";
import React, {useState} from "react";
import { View, TextInput, Button,Alert,Text,StyleSheet,TouchableOpacity, Image, ScrollView, KeyboardAvoidingView,Platform, } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
export default function App() {
  const [nome1, setNome1] = useState('');
  const [nome2, setNome2] = useState('');
  const [resultado, setResultado] = useState('');

  const preverbatalha = async () =>{
    if (!nome1 || !nome2){
      Alert.alert('Erro', 'Preencha os dois nomes de pokemon. ');
      return
    }
    try{
      const response = await fetch('http://192.168.1.71:8000/prever',{
        method: 'POST',
        headers:{
          'Content-Type' : 'application/json',
        },
        body: JSON.stringify({nome1,nome2})
      });
      const data = await response.json();
      if(response.ok){
        setResultado(`Vencedor: ${data.resultado}`)

      }else{
        Alert.alert('Erro', 'Erro na resposta da API.');
      }
    }catch(error){
      console.error(error);
      Alert.alert('Erro', 'Não foi possível conectar à API.')

    }
  };
  return (
    <LinearGradient
    colors={['#1a1a1a', '#2e2e2e', '#3a3a3a']}
    start={{x: 0, y: 0}}
    end={{x: 1, y: 1 }}
    style={styles.gradientBackground}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios'? 'padding' : undefined }
        >
        <ScrollView contentContainerStyle ={styles.scroll}>
          <Image
            source = {require('../assets/images/pokemon.jpg')}
            style={styles.topImage}
           resizeMode = "contain"
          /> 
          <Text style= {styles.title}>Batalha Pokemon</Text>
          <TextInput
            style={styles.input}
            placeholder="Digite o nome do primeiro pokemon"
            placeholderTextColor={'#999'}
            onChangeText={setNome1}
            value={nome1} />
          <TextInput
            style={styles.input}
            placeholder="Digite o nome do segundo pokemon"
            placeholderTextColor={'#999'}
            onChangeText={setNome2}
            value={nome2} />
          <LinearGradient
            colors={['#2e2e2e', '#444444', '#666666']}
            start={{x: 0, y: 0 }}
            end={{x: 1, y: 1}}
            style={styles.Batalha}>
            <TouchableOpacity onPress={preverbatalha}>
              <Text style={styles.batalhaText}> Iniciar batalha</Text>
            </TouchableOpacity>
          </LinearGradient>
          {resultado ? <Text style={styles.result}>{resultado}</Text> : null}
        </ScrollView>
      </KeyboardAvoidingView >
    </LinearGradient>
  );

}
const styles = StyleSheet.create({
  container: { flex: 1,backgroundColor:"#fff"},
  title: {fontSize:26, fontWeight: 'bold', textAlign: 'center', marginBottom:30, color:"#fff"},
  scroll: {padding: 20, alignItems:"center",justifyContent: "center"},
  topImage: {width: '100%',height: 250, marginBottom: 30},
  input: {
    width: '100%',
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#aaa',
    borderRadius: 8,
    padding: 12,
    marginBottom: 15,
  },
  button: {
    backgroundColor: '	#888888',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {color: '#fff', fontWeight:'bold' },
  Batalha:{
    width: "100%",
    backgroundColor: "#888888",
    padding: 15,
    borderRadius: 8,
    alignItems:'center'
  },
  batalhaText:{
    color: '#fff',
    fontWeight: 'bold',
  },
  result: {marginTop: 20,fontSize:25,textAlign:'center',color:"#fff"},
  gradientBackground:{
    flex: 1
  }
})
