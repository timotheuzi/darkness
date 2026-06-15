package com.darkness

import com.darkness.db.CacheDB
import com.darkness.db.CacheRepo
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest
import spock.lang.Specification

@DataJpaTest
class RepositoryTests extends Specification{

    @Autowired
    CacheRepo cacheRepo;

    def cacheEntity = new CacheDB(id: 1)

    def "find cache entry by Id" () {

        def savedCacheEntity  = cacheRepo.save(cacheEntity)

        when: "load entity"
        def newCacheEntity = cacheRepo.findById(savedCacheEntity.getId())

        then:"saved and retrieved entity by id must be equal"
        savedCacheEntity.getId() == newCacheEntity.getId()
    }
}