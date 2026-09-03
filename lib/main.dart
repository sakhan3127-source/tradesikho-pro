import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
void main()=>runApp(MaterialApp(debugShowCheckedModeBanner:false,home:MainScreen(),theme:ThemeData.dark()));
class MainScreen extends StatefulWidget{ @override State<MainScreen> createState()=>_MainScreenState(); }
class _MainScreenState extends State<MainScreen>{
int i=0;
var pages=[Dash(),Market(),Port(),Bot(),SetPage()];
@override Widget build(BuildContext c){return Scaffold(body:pages[i],bottomNavigationBar:BottomNavigationBar(currentIndex:i,onTap:(v)=>setState(()=>i=v),type:BottomNavigationBarType.fixed,items:[BottomNavigationBarItem(icon:Icon(Icons.dashboard),label:"Dash"),BottomNavigationBarItem(icon:Icon(Icons.show_chart),label:"NSE"),BottomNavigationBarItem(icon:Icon(Icons.pie_chart),label:"Port"),BottomNavigationBarItem(icon:Icon(Icons.smart_toy),label:"Bot"),BottomNavigationBarItem(icon:Icon(Icons.settings),label:"Set")]));}
}
class Dash extends StatelessWidget{ @override Widget build(BuildContext c){return Center(child:Text("TradeIndia PRO\nP&L +12450",style:TextStyle(fontSize:28)));} }
class Market extends StatelessWidget{
var list=["NIFTY","BANKNIFTY","RELIANCE","TCS","INFY","HDFCBANK","SBIN","ITC"];
@override Widget build(BuildContext c){return ListView.builder(itemCount:list.length,itemBuilder:(c,i){return ListTile(title:Text(list[i]),subtitle:Text("NSE Live"),trailing:Text("+1.2%",style:TextStyle(color:Colors.green)),onTap:(){Navigator.push(c,MaterialPageRoute(builder:(_)=>Detail(s:list[i])));});});}
}
class Detail extends StatelessWidget{
String s; Detail({required this.s});
@override Widget build(BuildContext c){return Scaffold(appBar:AppBar(title:Text(s)),body:Column(children:[Container(height:200,child:LineChart(LineChartData(lineBarsData:[LineChartBarData(spots:[FlSpot(0,1),FlSpot(1,2),FlSpot(2,1.5),FlSpot(3,3)],isCurved:true,color:Colors.green,barWidth:3,dotData:FlDotData(show:false))]))),ListTile(title:Text("AI Signal"),subtitle:Text("STRONG BUY 82%")),Row(children:[Expanded(child:ElevatedButton(onPressed:(){},child:Text("BUY"),style:ElevatedButton.styleFrom(backgroundColor:Colors.green))),SizedBox(width:10),Expanded(child:ElevatedButton(onPressed:(){},child:Text("SELL"),style:ElevatedButton.styleFrom(backgroundColor:Colors.red)))])]));}
}
class Port extends StatelessWidget{ @override Widget build(BuildContext c){return Center(child:Text("Portfolio"));}}
class Bot extends StatelessWidget{ @override Widget build(BuildContext c){return Center(child:Text("Auto Bot ON"));}}
class SetPage extends StatelessWidget{ @override Widget build(BuildContext c){return Center(child:Text("Settings"));}}
