package com.darkness.db;

import javax.persistence.*;
import java.time.LocalDateTime;

/**
 * High-performance transient state cache for game sectors.
 * Optimized for asynchronous lookups and reactive data flows.
 */
@Entity
@Table(name = "msg_cache", indexes = {
    @Index(name = "idx_map_name", columnList = "mapName")
})
public class CacheDB {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @Column(nullable = false)
    private String mapName;

    @Column(columnDefinition = "TEXT")
    private String currentRoomStatus;

    private LocalDateTime lastUpdated;

    public CacheDB() {
        this.lastUpdated = LocalDateTime.now();
    }

    public CacheDB(String mapName, String currentRoomStatus) {
        this.mapName = mapName;
        this.currentRoomStatus = currentRoomStatus;
        this.lastUpdated = LocalDateTime.now();
    }

    // Getters and Setters
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getMapName() {
        return mapName;
    }

    public void setMapName(String mapName) {
        this.mapName = mapName;
    }

    public String getCurrentRoomStatus() {
        return currentRoomStatus;
    }

    public void setCurrentRoomStatus(String currentRoomStatus) {
        this.currentRoomStatus = currentRoomStatus;
        this.lastUpdated = LocalDateTime.now();
    }

    public LocalDateTime getLastUpdated() {
        return lastUpdated;
    }

    public void setLastUpdated(LocalDateTime lastUpdated) {
        this.lastUpdated = lastUpdated;
    }

    @Override
    public String toString() {
        return "CacheDB{" +
                "id=" + id +
                ", mapName='" + mapName + '\'' +
                ", lastUpdated=" + lastUpdated +
                '}';
    }
}
