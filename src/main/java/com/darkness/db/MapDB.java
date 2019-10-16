package com.darkness.db;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

//map tables

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

	public MapDB() {

	}

	public MapDB(String name, String description, Integer items, Integer npcs, Integer users) {
		this.name = name;
		this.description = description;
		this.items = items;
		this.npcs = npcs;
		this.users = users;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getMapName() {
		return name;
	}

	public void setMapName(String name) {
		this.name = name;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public Integer getItems() {
		return items;
	}

	public void setItems(Integer items) {
		this.items = items;
	}

	public Integer getNpcs() {
		return npcs;
	}

	public void setNpcs(Integer npcs) {
		this.npcs = npcs;
	}

	public Integer getUsers() {
		return users;
	}

	public void setUsers(Integer users) {
		this.users = users;
	}

	public Object iterator() {
		// TODO Auto-generated method stub
		return null;
	}

	/*
	 * @Override public String toString() { return "User{" + ", name='" + name +
	 * '\'' + ", description=" + description + '}'; }
	 */
}