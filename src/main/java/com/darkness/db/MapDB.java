package com.darkness.db;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

//map tables

@Getter
@Setter
@Entity
@Table(name = "map")
public class MapDB {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private int id;

	private String name;
	private String description;
	private Integer items;
	private Integer npcs;
	private Integer users;

}