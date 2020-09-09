import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Data } from './Data'
import { from } from 'rxjs';
@Component({
  selector: 'app-client',
  templateUrl: './client.component.html',
  styleUrls: ['./client.component.css']
})
export class ClientComponent implements OnInit {
  public results:any;
  public jsonData:any;
  constructor(private http:HttpClient) { }
  Url: string = 'http://127.0.0.1:5000/show'
  header = ['_id','type','active','current','voltage','frequency','reactive','apparent','date','appliance','hour']
  nilm = []
  ngOnInit(): void {
    this.getData().subscribe(
      (resp) =>
      {
        this.nilm = resp;
        console.log(this.nilm)
      }
    )

 
    // this.http.get<Data>(this.Url).subscribe(data=>{
    //   this.results = data[0] ;
    //   console.log(this.results)
    // })
  }
  getData(){
    return this.http.get<Data[]>(this.Url)
  }
  
  
  

}
