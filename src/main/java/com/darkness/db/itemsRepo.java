package com.darkness.db;

import org.springframework.data.repository.CrudRepository;

import com.darkness.db.itemsDB;
 
public interface itemsRepo extends CrudRepository<itemsDB, Integer> 
{
	itemsDB findByName(String name);
}