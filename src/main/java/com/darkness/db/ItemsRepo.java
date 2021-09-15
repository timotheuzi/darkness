package com.darkness.db;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;

public interface ItemsRepo extends CrudRepository<ItemsDB, Integer> {
	ItemsDB findById(String id);

	//todo add custom query
	@Query("SELECT * FROM items where name = :name")
	Long selectByName(@Param("status") String name);
}