package com.darkness.db;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

//item table

@Entity
@Table(name = "msg_cache")
public class CacheDB {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private int id;
	private String mapName;
	private String currentRoomStatus;
}