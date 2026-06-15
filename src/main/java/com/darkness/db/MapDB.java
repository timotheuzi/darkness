package com.darkness.db;

import javax.persistence.*;

@Entity
@Table(name = "maps")
public class MapDB {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    private String name;
    private String description;
    private String exits; // JSON: {"north":1,"south":2,"east":3,"west":4}
    private String shop_name;
    private Integer npcs;
    private Integer users;
    private Integer items;
    private Integer safe_zone; // 0 or 1

    public MapDB() {}

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getExits() { return exits; }
    public void setExits(String exits) { this.exits = exits; }
    public String getShop_name() { return shop_name; }
    public void setShop_name(String shop_name) { this.shop_name = shop_name; }
    public Integer getNpcs() { return npcs; }
    public void setNpcs(Integer npcs) { this.npcs = npcs; }
    public Integer getUsers() { return users; }
    public void setUsers(Integer users) { this.users = users; }
    public Integer getItems() { return items; }
    public void setItems(Integer items) { this.items = items; }
    public Integer getSafe_zone() { return safe_zone; }
    public void setSafe_zone(Integer safe_zone) { this.safe_zone = safe_zone; }
}