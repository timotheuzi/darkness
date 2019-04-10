package com.darkness.db;

import javax.persistence.*;

//item table

@Entity
@Table(name = "msg_cache")
public class cacheDB
{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    private String mapName;
    private String currentRoomStatus;
 
    public cacheDB()
    {	
    	//this.id = id;
    }
    public int getId()
    {
        return id;
    }
    public void setId(int id)
    {
        this.id = id;
    }
    public cacheDB(String currentRoomStatus) 
    {
    	this.currentRoomStatus = currentRoomStatus;  
    }
 
    public String getCurrentStatis() 
    {
        return currentRoomStatus;
    }
    public void setCurrentStatus(String currentRoomStatus)
    {
        this.currentRoomStatus = currentRoomStatus;
    }
	public String getMapName() {
		return mapName;
	}
	public void setMapName(String mapName) {
		this.mapName = mapName;
	}
    
    /*@Override
    public String toString() 
    {
        return "User{" +
                ", currentStatus='" + currentStatus + '\'' +
                '}';
    }*/
}