
import 'package:flutter/material.dart';

class calc extends StatefulWidget {
  @override
  _calcState createState() => _calcState();
}

class _calcState extends State<calc> {
  int tipper = 0;
  int personc = 1;
  double amt = 0.0;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Bill Split"),
        centerTitle: true,
        backgroundColor: Colors.blue[400],
      ),
      body: Container(
        alignment: Alignment.center,
        color: Colors.white,
        child: ListView(
          scrollDirection: Axis.vertical,
          padding: EdgeInsets.all(20.2),
          children: <Widget>[
            Container(
              width: 150,
              height: 150,
              margin: EdgeInsets.only(
                  top: MediaQuery.of(context).size.height * 0.1),
              decoration: BoxDecoration(
                color: Colors.grey[200],
                borderRadius: BorderRadius.circular(12.0),
              ),
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[Text("Total per person",style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 20.0,)), Padding(
                      padding: const EdgeInsets.all(12.0),
                      child: Text(" ₹${calctotalperperson(amt,personc,tipper)}",style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: Colors.blue,
                      fontSize: 36.0,)),
                    )],
                ),
              ),
            ),
            Container(
              margin: EdgeInsets.only(top: 20.0),
              decoration: BoxDecoration(
                color: Colors.transparent,
                border: Border.all(
                  color: Colors.blueGrey.shade100,
                  style: BorderStyle.solid,
                ),
                borderRadius: BorderRadius.circular(12.0),
              ),
              child: Center(
                child: Column(
                  children: <Widget>[
                    TextField(
                        keyboardType:TextInputType.numberWithOptions(decimal: true),
                        style: TextStyle(color: Colors.blue, fontWeight: FontWeight.bold,fontSize: 20.0),
                        decoration: InputDecoration(
                          focusedBorder: UnderlineInputBorder(borderSide: BorderSide(color: Colors.grey)),
                          focusColor: Colors.green,
                          prefixText: "Bill Amount: ₹",
                          prefixIcon: Icon(Icons.attach_money),
                        ),
                        onChanged: (String value) {
                          try {
                            amt = double.parse(value);
                          } catch (exception) {
                            amt = 0.0;
                          }
                        }),
                         Padding(
                           padding: const EdgeInsets.only(left:8.0),
                           child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: <Widget>[
                            Text(
                              "Split",
                              style: TextStyle(
                                color: Colors.black54,
                                fontSize: 20.0,
                              ),
                            ),
                            Row(
                              children: <Widget>[
                                InkWell(
                                  onTap: () {
                                    setState(() {
                                      if (personc > 1) {
                                        personc--;
                                      }
                                    });
                                  },
                                  child: Container(
                                    width: 40.0,
                                    height: 40.0,
                                    margin: EdgeInsets.all(10.0),
                                    decoration: BoxDecoration(
                                      color: Colors.grey[200],
                                      borderRadius: BorderRadius.circular(12.0),
                                    ),
                                    child: Center(
                                      child: Text(
                                        "-",
                                        style: TextStyle(
                                          fontSize: 20.0,
                                          fontWeight: FontWeight.bold,
                                          color: Colors.black,
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                                Text("$personc",style: TextStyle(fontWeight: FontWeight.bold,fontSize: 20.0,color: Colors.blue),),
                                InkWell(
                                  onTap: () {
                                    setState(() {
                                      if (personc > 0) {
                                        personc++;
                                      }
                                    });
                                  },
                                  child: Container(
                                    width: 40.0,
                                    height: 40.0,
                                    margin: EdgeInsets.all(10.0),
                                    decoration: BoxDecoration(
                                      color: Colors.grey[200],
                                      borderRadius: BorderRadius.circular(12.0),
                                    ),
                                    child: Center(
                                      child: Text(
                                        "+",
                                        style: TextStyle(
                                          fontSize: 20.0,
                                          fontWeight: FontWeight.bold,
                                          color: Colors.black,
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                              ],
                            )
                        ],
                      ),
                         ),
                       Padding(
                         padding: const EdgeInsets.only(left:8.0, right: 15.0),
                         child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: <Widget>[
                            Text(
                              "Tip",
                              style: TextStyle(
                                color: Colors.black54,
                                fontSize: 20.0,
                              ),
                            ),
                            Text(
                              "₹${calctotaltip(amt, personc, tipper).toStringAsFixed(2)}",
                              style: TextStyle(
                                color: Colors.blue,
                                fontSize: 20.0,
                                fontWeight: FontWeight.bold
                              ),
                            ),
                          ],
                      ),
                       ),
                     Padding(
                       padding: const EdgeInsets.only(top:30.0),
                       child: Column(
                         children: <Widget>[
                           Text("$tipper%",style: TextStyle(
                             fontSize: 24.0,
                             fontWeight: FontWeight.bold,
                             color: Colors.blue),),

                             Slider(min:0, max:100, activeColor: Colors.blue, inactiveColor:Colors.grey, value:tipper.toDouble(), onChanged: (double value){
                               setState(() {
                                 tipper= value.round();
                               });
                             })
                         ],
                       ),
                     ),
                  ],
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
  calctotalperperson(double billamt, int splitby,int tipper){
     var totalperperson= (calctotaltip(billamt,splitby,tipper) +billamt)/splitby;
     return totalperperson.toStringAsFixed(2);
  }
  calctotaltip(double billamt, int splitby,int tipper){
    double totaltip=0.0;

    if(billamt<0 || billamt.toString().isEmpty || billamt==null){

    } else{
       totaltip = (amt*tipper)/100;
    }
   return totaltip;
  }
}
